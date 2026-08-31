import api from "./client";


// =========================================================
// 회원가입
// =========================================================

export async function signup(
    username,
    email,
    password,
) {

    const response = await api.post(
        "/auth/signup",
        {
            username,
            email,
            password,
        },
    );

    return response.data;
}


// =========================================================
// 로그인
// =========================================================

export async function login(
    username,
    password,
) {

    const response = await api.post(
        "/auth/login",
        {
            username,
            password,
        },
    );

    return response.data;
}

// =========================================================
// 로그아웃
// =========================================================

export async function logout(
    userId,
) {

    const response = await api.post(
        `/auth/logout?user_id=${userId}`,
    );

    return response.data;
}