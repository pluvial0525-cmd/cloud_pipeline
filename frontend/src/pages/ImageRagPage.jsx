import styled from "styled-components";

import ImageUpload
    from "../components/ImageUpload";

import ImageResult
    from "../components/ImageResult";

import {
    logout,
} from "../api/authApi";

import {
    useImageRagMutation,
} from "../query/imageRagQuery";


function ImageRagPage() {

    const imageRagMutation =
        useImageRagMutation();


    const user = JSON.parse(
        localStorage.getItem(
            "user"
        )
        || "null"
    );


    // =====================================================
    // Image RAG 검색
    // =====================================================

    const handleSearch = (
        file,
    ) => {

        imageRagMutation.mutate({
            file,
            topK: 5,
        });

    };


    // =====================================================
    // 로그아웃
    // =====================================================

    const handleLogout = async () => {

        try {

            if (user?.id) {

                await logout(
                    user.id
                );

            }

        } catch (error) {

            console.error(
                "로그아웃 API 오류:",
                error
            );

        } finally {

            // ================================================
            // 브라우저 로그인 정보 삭제
            // ================================================

            localStorage.removeItem(
                "access_token"
            );

            localStorage.removeItem(
                "user"
            );


            // ================================================
            // 로그인 페이지로 완전히 이동
            // ================================================

            window.location.href =
                "/login";

        }

    };


    return (
        <Page>
            <Container>

                <TopBar>
                    <UserInfo>
                        {
                            user?.username
                                ? `${user.username}님`
                                : "사용자"
                        }
                    </UserInfo>

                    <LogoutButton
                        onClick={
                            handleLogout
                        }
                    >
                        로그아웃
                    </LogoutButton>
                </TopBar>


                <Header>
                    <Badge>
                        IMAGE RAG
                    </Badge>

                    <Title>
                        Korean Food
                        Image Search
                    </Title>

                    <Subtitle>
                        음식 이미지를
                        업로드하면
                        OpenAI Vision과
                        임베딩을 이용해
                        가장 유사한 음식
                        이미지를 검색합니다.
                    </Subtitle>
                </Header>


                <Content>
                    <ImageUpload
                        onSearch={
                            handleSearch
                        }
                        isPending={
                            imageRagMutation
                                .isPending
                        }
                    />

                    <ImageResult
                        data={
                            imageRagMutation
                                .data
                        }
                    />
                </Content>


                {
                    imageRagMutation
                        .isError
                    && (
                        <ErrorBox>
                            검색 중 오류가
                            발생했습니다.

                            <br />

                            {
                                imageRagMutation
                                    .error
                                    ?.response
                                    ?.data
                                    ?.detail
                                ||
                                imageRagMutation
                                    .error
                                    ?.message
                            }
                        </ErrorBox>
                    )
                }

            </Container>
        </Page>
    );
}


export default ImageRagPage;


/* =========================================================
   Style
========================================================= */

const Page = styled.div`
    min-height: 100vh;

    background:
            radial-gradient(
                    circle at top,
                    #1b2035 0%,
                    #0d1017 42%,
                    #080a0f 100%
            );

    color: white;
`;


const Container = styled.div`
    width: min(
            1180px,
            calc(
                    100% - 40px
            )
    );

    margin: 0 auto;

    padding: 35px 0 70px;
`;


/* =========================================================
   Top Bar
========================================================= */

const TopBar = styled.div`
    display: flex;

    align-items: center;
    justify-content: flex-end;

    gap: 14px;

    margin-bottom: 35px;
`;


const UserInfo = styled.div`
    color: #929baa;

    font-size: 14px;
`;


const LogoutButton = styled.button`
    padding: 10px 16px;

    border-radius: 10px;

    border: 1px solid
    rgba(
            255,
            255,
            255,
            0.1
    );

    background: #151a23;

    color: white;

    font-size: 14px;

    cursor: pointer;

    transition: 0.2s;

    &:hover {
        border-color: #8170ff;

        background: #1b2130;
    }
`;


/* =========================================================
   Header
========================================================= */

const Header = styled.div`
    margin-bottom: 45px;
`;


const Badge = styled.div`
    display: inline-block;

    margin-bottom: 12px;

    padding: 7px 12px;

    border-radius: 100px;

    background:
        rgba(
            124,
            92,
            255,
            0.15
        );

    border: 1px solid
        rgba(
            124,
            92,
            255,
            0.3
        );

    color: #9587ff;

    font-size: 11px;
    font-weight: 800;

    letter-spacing: 1.5px;
`;


const Title = styled.h1`
    margin: 0;

    font-size:
        clamp(
            38px,
            5vw,
            66px
        );

    letter-spacing: -2px;
`;


const Subtitle = styled.p`
    width: min(
        650px,
        100%
    );

    margin-top: 16px;

    color: #929baa;

    font-size: 16px;

    line-height: 1.7;
`;


/* =========================================================
   Content
========================================================= */

const Content = styled.div`
    display: grid;

    grid-template-columns:
        minmax(
            0,
            0.9fr
        )
        minmax(
            0,
            1.1fr
        );

    gap: 25px;

    align-items: start;

    @media (
        max-width: 950px
    ) {
        grid-template-columns:
            1fr;
    }
`;


/* =========================================================
   Error
========================================================= */

const ErrorBox = styled.div`
    margin-top: 20px;

    padding: 18px;

    border-radius: 14px;

    border: 1px solid
    rgba(
            255,
            90,
            90,
            0.3
    );

    background:
            rgba(
                    255,
                    90,
                    90,
                    0.08
            );

    color: #ff9b9b;

    line-height: 1.6;
`;