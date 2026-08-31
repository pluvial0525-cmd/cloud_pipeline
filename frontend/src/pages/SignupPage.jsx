import {
    useState,
} from "react";

import {
    useNavigate,
} from "react-router-dom";

import styled from "styled-components";

import {
    signup,
} from "../api/authApi";


function SignupPage() {

    const navigate = useNavigate();

    const [
        username,
        setUsername,
    ] = useState("");

    const [
        email,
        setEmail,
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

            await signup(
                username,
                email,
                password,
            );

            alert(
                "회원가입이 완료되었습니다."
            );

            navigate(
                "/login"
            );

        } catch (error) {

            const message =
                error?.response?.data?.detail
                || "회원가입에 실패했습니다.";

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
            <SignupCard>
                <Title>
                    회원가입
                </Title>

                <Subtitle>
                    새 계정을 만들어주세요.
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
                            value={
                                username
                            }
                            onChange={
                                (
                                    event
                                ) =>
                                    setUsername(
                                        event.target.value
                                    )
                            }
                            placeholder="username"
                        />
                    </Field>

                    <Field>
                        <Label>
                            이메일
                        </Label>

                        <Input
                            type="email"
                            value={
                                email
                            }
                            onChange={
                                (
                                    event
                                ) =>
                                    setEmail(
                                        event.target.value
                                    )
                            }
                            placeholder="email"
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
                                        event.target.value
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

                    <SignupButton
                        type="submit"
                        disabled={
                            loading
                        }
                    >
                        {
                            loading
                                ? "가입 중..."
                                : "회원가입"
                        }
                    </SignupButton>

                    <LoginLink
                        type="button"
                        onClick={
                            () =>
                                navigate(
                                    "/login"
                                )
                        }
                    >
                        로그인으로 돌아가기
                    </LoginLink>
                </Form>
            </SignupCard>
        </Page>
    );

}


export default SignupPage;


const Page = styled.div`
    min-height: 100vh;

    display: flex;
    align-items: center;
    justify-content: center;

    background: #0b0f17;

    padding: 20px;
`;


const SignupCard = styled.div`
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
`;


const SignupButton = styled.button`
    padding: 14px;

    border: none;

    border-radius: 12px;

    background: #6f5cff;

    color: white;

    font-weight: 700;

    cursor: pointer;
`;


const LoginLink = styled.button`
    background: transparent;

    border: none;

    color: #8170ff;

    cursor: pointer;
`;