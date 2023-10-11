# [CI4] ci4-admin / ion-auth 적용하기.

```
    개발을 하다보면 관리자 , 회원가입 부분을 개발해야 하는데 이미 잘 만들어져있는 모듈을 사용하자.
```
##  ci4-admin 설치
```
    composer require bvrignaud/ci4-admin

    or

    git clone https://github.com/bvrignaud/ci4-admin.git
```

##  CodeIgniter-Ion-Auth 설치
```
    composer init
    composer config minimum-stability dev
    composer config repositories.ionAuth vcs git@github.com:benedmunds/CodeIgniter-Ion-Auth.git
    composer require benedmunds/codeigniter-ion-auth:4.x-dev    

    or

    git clone https://github.com/benedmunds/CodeIgniter-Ion-Auth.git
    cd CodeIgniter-Ion-Auth
    git checkout 4
```

## 설정
```php
    Config/Autoload.php
    
    public $psr4 = [
        'App'         => APPPATH,                // To ensure filters, etc still found,
        APP_NAMESPACE => APPPATH, // For custom app namespace
        'Config'      => APPPATH . 'Config',
        'IonAuth' => ROOTPATH . 'CodeIgniter-Ion-Auth',
        'Admin'   => ROOTPATH . 'ci4-admin',
    ];

```
## assets 
```
    cd public/assets
    yarn add admin-lte@v3
```

## IonAuth.php
```php
    Config/IonAuth.php 파일 생성
        
        <?php namespace Config;

        class IonAuth extends \IonAuth\Config\IonAuth
        {
            // set your specific config
            // public $siteTitle                = 'Example.com';       // Site Title, example.com
            // public $adminEmail               = 'admin@example.com'; // Admin Email, admin@example.com
            // public $emailTemplates           = 'App\\Views\\auth\\email\\';
            // ...
        }    
```

## Auth.php
```php
    Controllers/Auth.php 파일 생성
        
        <?php namespace App\Controllers;

        class Auth extends \IonAuth\Controllers\Auth
        {
            /**
             * If you want to customize the views,
             *  - copy the ion-auth/Views/auth folder to your Views folder,
             *  - remove comment
             */
            // protected $viewsFolder = 'auth';
        } 
```

## DB SetUp
```
    .env 파일 생성 후 db연결
    php spark migrate -n IonAuth
    
    php spark db:seed IonAuth\Database\Seeds\IonAuthSeeder

    linux

    php spark db:seed IonAuth\\Database\\Seeds\\IonAuthSeeder
```

## Router 추가
```php
    $routes->group('auth', ['namespace' => 'IonAuth\Controllers'], function ($routes) {
        $routes->add('login', 'Auth::login');
        $routes->get('logout', 'Auth::logout');
        $routes->add('forgot_password', 'Auth::forgot_password');
        // $routes->get('/', 'Auth::index');
        // $routes->add('create_user', 'Auth::create_user');
        // $routes->add('edit_user/(:num)', 'Auth::edit_user/$1');
        // $routes->add('create_group', 'Auth::create_group');
        // $routes->get('activate/(:num)', 'Auth::activate/$1');
        // $routes->get('activate/(:num)/(:hash)', 'Auth::activate/$1/$2');
        // $routes->add('deactivate/(:num)', 'Auth::deactivate/$1');
        // $routes->get('reset_password/(:hash)', 'Auth::reset_password/$1');
        // $routes->post('reset_password/(:hash)', 'Auth::reset_password/$1');
        // ...
    });
    $routes->group('admin', ['namespace' => 'Admin\Controllers'], function ($routes) {
        $routes->get('/', 'Home::index');

        $routes->group('users', ['namespace' => 'Admin\Controllers'], function ($routes) {
            $routes->get('/', 'Users::index');
            $routes->add('create', 'Users::createUser');
            $routes->add('edit/(:num)', 'Users::edit/$1');
            $routes->add('activate/(:num)', 'Users::activate/$1');
            $routes->add('deactivate/(:num)', 'Users::deactivate/$1');
            $routes->add('edit_group/(:num)', 'Users::editGroup/$1');
            $routes->add('create_group', 'Users::createGroup');
        });

        $routes->group('informations', ['namespace' => 'Admin\Controllers'], function ($routes) {
            $routes->get('/', 'Informations::index');
            $routes->get('displayPhpInfo', 'Informations::displayPhpInfo');
            $routes->add('exportDatabase', 'Informations::exportDatabase');
            $routes->post('sendEmailForTest', 'Informations::sendEmailForTest');
        });
    });    
```




