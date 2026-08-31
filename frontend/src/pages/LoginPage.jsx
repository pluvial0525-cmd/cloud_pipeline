import {
    useState,
} from "react";

import {
    useNavigate,
} from "react-router-dom";

import styled from "styled-components";

import {
    login,
} from "../api/authApi";


function LoginPage() {

    const navigate = useNavigate();

    const [
        username,
        setUsername,
    ] = useState("");

    const [
        password,
        setPassword,
    ] = useState("");

    const [
        error,
        setError,
    ] = useState("");

    const [
        loading,
        setLoading,
    ] = useState(false);


    const handleSubmit = async (
        event,
    ) => {

        event.preventDefault();

        setError("");

        setLoading(true);

        try {

            const data = await login(
                username,
                password,
            );


            localStorage.setItem(
                "access_token",
                data.access_token,
            );

            localStorage.setItem(
                "user",
                JSON.stringify(
                    data.user,
                ),
            );


// 로그인 완료 후 메인 페이지 새로 로드
            window.location.href = "/";

        } catch (error) {

            const message =
                error?.response?.data?.detail
                || "로그인에 실패했습니다.";

            setError(
                message
            );

        } finally {

            setLoading(
                false
            );

        }

    };


    return (
        <Page>
            <LoginCard>
                <Title>
                    로그인
                </Title>

                <Subtitle>
                    Image RAG 서비스를
                    이용하려면 로그인해주세요.
                </Subtitle>


                <Form
                    onSubmit={
                        handleSubmit
                    }
                >
                    <Field>
                        <Label>
                            사용자 이름
                        </Label>

                        <Input
                            type="text"
                            value={
                                username
                            }
                            onChange={
                                (
                                    event
                                ) =>
                                    setUsername(
                                        event
                                            .target
                                            .value
                                    )
                            }
                            placeholder="username"
                        />
                    </Field>


                    <Field>
                        <Label>
                            비밀번호
                        </Label>

                        <Input
                            type="password"
                            value={
                                password
                            }
                            onChange={
                                (
                                    event
                                ) =>
                                    setPassword(
                                        event
                                            .target
                                            .value
                                    )
                            }
                            placeholder="password"
                        />
                    </Field>


                    {
                        error
                        && (
                            <ErrorMessage>
                                {
                                    error
                                }
                            </ErrorMessage>
                        )
                    }


                    <LoginButton
                        type="submit"
                        disabled={
                            loading
                        }
                    >
                        {
                            loading
                                ? "로그인 중..."
                                : "로그인"
                        }
                    </LoginButton>


                    <SignupLink
                        type="button"
                        onClick={
                            () =>
                                navigate(
                                    "/signup"
                                )
                        }
                    >
                        회원가입
                    </SignupLink>
                </Form>
            </LoginCard>
        </Page>
    );

}


export default LoginPage;


/* =========================================================
   Style
========================================================= */

const Page = styled.div`
    min-height: 100vh;

    display: flex;

    align-items: center;
    justify-content: center;

    background: #0b0f17;

    padding: 20px;
`;


const LoginCard = styled.div`
    width: 100%;
    max-width: 420px;

    padding: 36px;

    border-radius: 24px;

    background: #151a23;

    border: 1px solid
    rgba(
            255,
            255,
            255,
            0.08
    );
`;


const Title = styled.h1`
    margin: 0;

    color: white;

    font-size: 32px;
`;


const Subtitle = styled.p`
    margin-top: 12px;
    margin-bottom: 28px;

    color: #8d96a5;

    line-height: 1.6;
`;


const Form = styled.form`
    display: flex;

    flex-direction: column;

    gap: 20px;
`;


const Field = styled.div`
    display: flex;

    flex-direction: column;

    gap: 8px;
`;


const Label = styled.label`
    color: #d7dbe3;

    font-size: 14px;

    font-weight: 600;
`;


const Input = styled.input`
    width: 100%;

    box-sizing: border-box;

    padding: 14px 16px;

    border-radius: 12px;

    border: 1px solid
    rgba(
            255,
            255,
            255,
            0.1
    );

    background: #0f141d;

    color: white;

    outline: none;

    font-size: 15px;

    &:focus {
        border-color: #8170ff;
    }
`;


const ErrorMessage = styled.div`
    padding: 12px;

    border-radius: 10px;

    background:
            rgba(
                    255,
                    80,
                    80,
                    0.1
            );

    color: #ff8f8f;

    font-size: 14px;
`;


const LoginButton = styled.button`
    padding: 14px;

    border: none;

    border-radius: 12px;

    background: #6f5cff;

    color: white;

    font-size: 15px;

    font-weight: 700;

    cursor: pointer;

    &:disabled {
        opacity: 0.6;

        cursor: not-allowed;
    }
`;


const SignupLink = styled.button`
    padding: 4px;

    border: none;

    background: transparent;

    color: #8170ff;

    font-size: 14px;

    cursor: pointer;

    &:hover {
        text-decoration: underline;
    }
`;