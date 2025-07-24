# [NodeJS] express / 정적파일 캐시 설정하기 / 반짝 거리는거 제어

## 이유
```
node로 front를 개발하다보니 페이지 이동이나 새로고침시 이미지 파일들의 로드가 오래 걸려서 
화면이 반짝 거리는 걸 확인했다.
```

## 소스
```ts
app.use('/uploads', express.static(path.join(__dirname, '../public/uploads'), {
    maxAge: '0', // 또는 '1m' 정도로 짧게
    etag: false
}));

// 나머지 public은 캐시 강하게
app.use(express.static(path.join(__dirname, '../public'), {
    maxAge: '7d',
    etag: false, // "조건부 요청 생략, 속도 향상
    immutable: true // "절대 안 바뀐다"고 선언해서 브라우저가 더 적극적으로 캐시함
}));
```

## 설명
```
변할 수 있는 파일은 매번 불러오고, 안 변하는 파일은 캐시하자
```