# [Git] push 오류 시 해결하기

## 
```
가끔 push 할 때 이런 오류가 나온다.

On branch main Your branch is up to date with 'origin/main'. 

nothing to commit, working tree clean

```

## 해결 방법
```
1. rm -rf .git/
2. git init
3. git add .
4. git commit -m ''
5. git remote add origin '주소'
6. git push -f origin main

```


git remote set-url origin https://계정이름@github.com/~~~