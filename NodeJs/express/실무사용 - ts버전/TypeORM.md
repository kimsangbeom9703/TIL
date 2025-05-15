# [NodeJS] TypeORM 사용하기

## 사용이유
1. 다양한 DB지원 : MySQL, PostgreSQL, SQLite, MariaDB, Oracle, SQL Server 등 지원
2. 객체 지향 방식의 db 작업
3. 타입 안정성
4. 쿼리 작성이 쉬움

## 설치
```bash
npm install typeorm reflect-metadata mysql2
npm install -D @types/node
```

## 프로젝트 구성 예시
```
src/
├── config/
│   └── data-source.ts
├── entities/
│   └── User.ts
├── routes/
│   └── userRoutes.ts
├── controllers/
│   └── userController.ts
├── index.ts
```

## config/data-source.ts
```ts
import 'reflect-metadata';
import {DataSource} from 'typeorm';
import {User} from '../entities/user.entity'; // 이후 엔티티들 여기에 추가

import {ENV} from './env';

export const AppDataSource = new DataSource({
    type: ENV.DB_TYPE as 'mysql' | 'mariadb' | 'postgres' | 'sqlite' | 'mssql', // 등등 필요에 따라
    host: ENV.DB_HOST,
    port: parseInt(ENV.DB_PORT, 10), // 문자열을 숫자로 변환
    username: ENV.DB_USER,
    password: ENV.DB_PASS,
    database: ENV.DB_NAME,
    synchronize: true,
    logging: false,
    entities: [User],
});
```
## entities/User.ts
```ts
import {Entity, PrimaryGeneratedColumn, Column, CreateDateColumn, UpdateDateColumn, DeleteDateColumn} from 'typeorm';

@Entity('tb_users')
export class User {
    @PrimaryGeneratedColumn()
    id: number;

    @Column({unique: true})
    user_id: string;

    @Column()
    user_name: string;

    @Column()
    password: string;

    @Column()
    password_salt: string;

    @Column({nullable: true})
    role_id: number;

    @Column({default: true})
    is_active: boolean;

    @Column({nullable: true})
    user_email: string;

    @Column({nullable: true})
    phone: string;

    @Column({nullable: true})
    company: string;

    @CreateDateColumn()
    created_at: Date;

    @UpdateDateColumn()
    updated_at: Date;

    @DeleteDateColumn()
    deleted_at: Date;
}
```

## root/app.ts
```ts
import { AppDataSource } from './config/data-source';
AppDataSource.initialize()
    .then(() => {
        console.log('DB 연결 성공');
    })
    .catch((error) => console.log('DB 연결 실패', error));
```

## 로그인 예시 route
```ts
import express from 'express';
import { login, logout ,showLoginPage } from '../controllers/auth.controller';

const router = express.Router();

// 로그인 라우트
router.get('/login', showLoginPage);
router.post('/login', login);

// 로그아웃 라우트
router.get('/logout', logout);

export default router;
```

## 로그인 예시 controllers
```ts
import {Request, Response, RequestHandler} from 'express'; // express에서 타입 가져오기
import AuthService from '../services/auth.service';

const login: RequestHandler = async (req: Request, res: Response): Promise<void> => {
    const {user_id, password} = req.body;

    if (!user_id || !password) {
        res.status(400).render('auth/login', {error: 'user_id와 password를 모두 입력해주세요.'});
        return;
    }

    try {
        const user = await AuthService.login(user_id, password);

        req.session.user = {
            id: user.id,
            user_id: user.user_id,
            user_name: user.user_name,
            role_id: user.role_id,
            is_active: user.is_active
        };

        res.redirect('/admin'); // 로그인 성공 시 리다이렉트
    } catch (err: unknown) {
        // err가 Error 타입인지 확인
        if (err instanceof Error) {
            res.status(401).render('auth/login', {error: err.message});
        } else {
            // 만약 err가 Error 객체가 아니라면 기본 메시지 처리
            res.status(500).render('auth/login', {error: '알 수 없는 오류가 발생했습니다.'});
        }
    }
};
```

## 로그인 예시 service
```ts
// src/services/auth.service.ts
import { AppDataSource } from '../../config/data-source';
import { User } from '../../entities/user.entity';
import bcrypt from 'bcrypt';

class AuthService {
    // 로그인 처리
    async login(user_id: string, password: string) {
        const userRepository = AppDataSource.getRepository(User);
        const user = await userRepository.findOne({ where: { user_id } });

        if (!user) {
            throw new Error('사용자를 찾을 수 없습니다.');
        }

        if (!user.password) {
            throw new Error('서버 오류: 사용자 비밀번호가 없습니다.');
        }

        const isMatch = await bcrypt.compare(password, user.password);

        if (!isMatch) {
            throw new Error('비밀번호가 일치하지 않습니다.');
        }

        return user;
    }

    // 로그아웃 처리
    logout(session: any) {
        session.destroy((err: any) => {
            if (err) {
                throw new Error('로그아웃 실패');
            }
        });
    }
}
export default new AuthService();
```