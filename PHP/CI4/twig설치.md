# [CI4] Twig 템플릿 엔진 설치하기

## twig 설치
<https://github.com/daycry/twig>

```
    composer require daycry/twig
```

## 설정
```php
config/service

public static function twig(?TwigConfig $config = new TwigConfig(), bool $getShared = true){
    if ($getShared) {
        return static::getSharedInstance('twig', $config);
    }
    $config ??= config('Twig');
    $twig = new Twig($config);
    $twig->addGlobal('ADMIN_VIEW_MAIN_PATH',ADMIN_VIEW_MAIN_PATH);
    $twig->addGlobal('ADMIN_VIEW_PATH',ADMIN_VIEW_PATH);
    $twig->addGlobal('ADMIN_URL_PREFIX',ADMIN_URL_PREFIX);
    
    $twig->addGlobal('HOME_VIEW_MAIN_PATH',HOME_VIEW_MAIN_PATH);
    $twig->addGlobal('HOME_VIEW_PATH',HOME_VIEW_PATH);
    
    $twig->addGlobal('AUTH_URL_PREFIX',AUTH_URL_PREFIX);
    
    $twig->addGlobal('ENV',$_ENV);
    return $twig;
}
```

```php
    Libraries/Twig
    <?php

    namespace App\Libraries\Twig;

    use App\Libraries\Twig\TwigConfig;
    use Config\Services;
    use Twig\Environment;
    use Twig\Extension\DebugExtension;
    use Twig\Loader\FilesystemLoader;
    use Twig\Loader\LoaderInterface;
    use Twig\TwigFunction;

    use App\Controllers\Common;

    //php spark cache:clear
    class Twig
    {
        //    private int $ttl = 3600;
        /**
         * @var array Paths to Twig templates
         */
        private array $paths = [APPPATH . 'Views'];
        
        /**
         * @var array Functions to add to Twig
         */
        private array $functions_asis = ['base_url', 'site_url'];
        
        /**
         * @var array Functions with `is_safe` option
         *
         * @see http://twig.sensiolabs.org/doc/advanced.html#automatic-escaping
         */
        private array $functions_safe = [
            'form_open', 'form_close', 'form_textarea', 'sprintf', 'form_error', 'form_input', 'form_label', 'form_hidden', 'set_value', 'form_dropdown', 'form_submit', 'lang',
        ];
        
        /**
         * @var array Twig Environment Options
         *
         * @see http://twig.sensiolabs.org/doc/api.html#environment-options
         */
        private array $config = [];
        
        /**
         * @var bool Whether functions are added or not
         */
        private bool $functions_added = false;
        
        private ?Environment     $twig   = null;
        private ?LoaderInterface $loader = null;
        
        public function __construct(?TwigConfig $config = null)
        {
            helper('form');
            $this->initialize($config);
            $this->deleteExpiredTwigCache();
        }
        
        public function initialize(?TwigConfig $config = null)
        {
            if (empty($config)) {
                $config = config('Twig');
            }
            
            if (isset($config->functions_asis)) {
                $this->functions_asis = array_unique(array_merge($this->functions_asis, $config->functions_asis));
            }
            
            if (isset($config->functions_safe)) {
                $this->functions_safe = array_unique(array_merge($this->functions_safe, $config->functions_safe));
            }
            if (isset($config->paths)) {
                $this->paths = array_unique(array_merge($this->paths, $config->paths));
            }
            
            // default Twig config
            $this->config = [
                'cache'          => WRITEPATH . 'cache' . DIRECTORY_SEPARATOR . 'twig',
                'debug'          => ENVIRONMENT !== 'production',
                'autoescape'     => 'html',
                'cache_lifetime' => 3600, // 캐시 TTL 설정 (1 시간)
            ];
        }
        
        public function deleteExpiredTwigCache()
        {
            $cache = \Config\Services::cache();
            $cacheFiles = glob($this->config['cache'] . '/*/*.php', GLOB_NOSORT);
            $currentTimestamp = time();
            
            foreach ($cacheFiles as $cacheFile) {
                // 파일의 마지막 수정 시간을 가져옵니다.
                $fileTimestamp = @filemtime($cacheFile);
                
                // 파일의 만료 여부를 확인하고, TTL보다 오래된 파일은 삭제합니다.
                if ($currentTimestamp - $fileTimestamp >= $this->config['cache_lifetime']) {
                    //                unlink($cacheFile); // 캐시 파일 삭제
                    $cache->clean();
                }
            }
        }
        
        public function resetTwig()
        {
            $this->twig = null;
            $this->createTwig();
        }
        
        protected function createTwig()
        {
            // $this->twig is singleton
            if ($this->twig !== null) {
                return;
            }
            
            if ($this->loader === null) {
                $this->loader = new FilesystemLoader($this->paths);
            }
            
            $twig = new Environment($this->loader, $this->config);
            
            if ($this->config['debug']) {
                $twig->addExtension(new DebugExtension());
            }
            
            $this->twig = $twig;
            
        }
        
        protected function setLoader($loader)
        {
            $this->loader = $loader;
        }
        
        /**
         * Registers a Global
         *
         * @param string $name The global name
         * @param mixed $value The global value
         */
        public function addGlobal($name, $value)
        {
            $this->createTwig();
            $this->twig->addGlobal($name, $value);
        }
        
        protected function addFunctions()
        {
            // Runs only once
            if ($this->functions_added) {
                return;
            }
            
            // as is functions
            foreach ($this->functions_asis as $function) {
                if (function_exists($function)) {
                    $this->twig->addFunction(new TwigFunction($function, $function));
                }
            }
            
            // safe functions
            foreach ($this->functions_safe as $function) {
                if (function_exists($function)) {
                    $this->twig->addFunction(new TwigFunction($function, $function, ['is_safe' => ['html']]));
                }
            }
            
            // customized functions
            if (function_exists('anchor')) {
                $this->twig->addFunction(new TwigFunction('anchor', [$this, 'safe_anchor'], ['is_safe' => ['html']]));
            }
            
            $this->twig->addFunction(new TwigFunction('validation_list_errors', [$this, 'validation_list_errors'], ['is_safe' => ['html']]));
            
            $this->functions_added = true;
        }
        
        /**
         * @param string $uri
         * @param string $title
         * @param array $attributes [changed] only array is acceptable
         */
        public function safe_anchor($uri = '', $title = '', $attributes = []): string
        {
            $uri = esc($uri, 'url');
            $title = esc($title);
            
            $new_attr = [];
            
            foreach ($attributes as $key => $val) {
                $new_attr[esc($key)] = $val;
            }
            
            return anchor($uri, $title, $new_attr);
        }
        
        /**
         * @codeCoverageIgnore
         */
        public function validation_list_errors(): string
        {
            return Services::validation()->listErrors();
        }
        
        public function getTwig(): Environment
        {
            $this->createTwig();
            
            return $this->twig;
        }
        
        /**
         * @return array
         */
        public function getPaths()
        {
            return $this->paths;
        }
        
        /**
         * Renders Twig Template and Set Output
         *
         * @param string $view Template filename without `.twig`
         * @param array $params Array of parameters to pass to the template
         */
        public function display(string $view, array $params = [])
        {
            echo $this->render($view, $params);
        }
        
        /**
         * Renders Twig Template and Returns as String
         *
         * @param string $view Template filename without `.twig`
         * @param array $params Array of parameters to pass to the template
         */
        public function render(string $view, array $params = []): string
        {
            $this->createTwig();
            // We call addFunctions() here, because we must call addFunctions()
            // after loading CodeIgniter functions in a controller.
            $this->addFunctions();
            
            $view = $view . '.twig';
            
            return $this->twig->render($view, $params);
        }
    }
```
```php
Libraries/TwigConfig
    <?php

    namespace App\Libraries\Twig;
    use CodeIgniter\Config\BaseConfig;

    class TwigConfig extends BaseConfig
    {
        public $functions_safe = ['pathvariable', 'config', 'number_format', 'fileUrl','date_string_format', 'csrf_field','admin_site_url'];
        public $functions_asis = ['current_url', 'base_url','site_url','count','intval','date_format','base64encode','base64decode'];
        public $paths          = [];
    //    public $ttl = 1; // 1 hour (for example)
    } 
```
```php
Controllers\Main\MainBaseController
    protected function render(string $path, $datas = []): string
    {
        return service('twig')->render(HOME_VIEW_PATH . $path, $datas);
    }
    
    protected function view(string $body): string
    {
        $datas = [
            'body' => $body,
        ];
        return service('twig')->render(HOME_VIEW_MAIN_PATH, $datas);
    }
```


