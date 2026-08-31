import styled from "styled-components";


function ImageResult({
                         data,
                     }) {
    if (!data) {
        return (
            <EmptyCard>
                검색 결과가
                여기에 표시됩니다.
            </EmptyCard>
        );
    }


    return (
        <ResultWrapper>
            <AnalysisCard>
                <SectionLabel>
                    OpenAI 이미지 분석
                </SectionLabel>

                <AnalysisText>
                    {
                        data.query_description
                    }
                </AnalysisText>
            </AnalysisCard>


            <ResultHeader>
                <div>
                    <SectionLabel>
                        유사 이미지
                    </SectionLabel>

                    <ResultTitle>
                        Top {
                        data.results?.length
                    }
                    </ResultTitle>
                </div>
            </ResultHeader>


            <ResultGrid>
                {data.results?.map(
                    (item) => (
                        <ResultCard
                            key={
                                `${item.rank}-${item.image_path}`
                            }
                        >
                            {/* S3 이미지 */}
                            {item.image_url && (
                                <ImageWrapper>
                                    <ResultImage
                                        src={item.image_url}
                                        alt={item.food_name}
                                    />
                                </ImageWrapper>
                            )}


                            <CardContent>
                                <Rank>
                                    #
                                    {
                                        item.rank
                                    }
                                </Rank>

                                <FoodName>
                                    {
                                        item.food_name
                                    }
                                </FoodName>

                                <Similarity>
                                    유사도{" "}

                                    <strong>
                                        {(
                                            item.similarity
                                            * 100
                                        ).toFixed(
                                            1,
                                        )}
                                        %
                                    </strong>
                                </Similarity>

                                <Path>
                                    {
                                        item.image_path
                                    }
                                </Path>
                            </CardContent>
                        </ResultCard>
                    ),
                )}
            </ResultGrid>
        </ResultWrapper>
    );
}


export default ImageResult;


const ResultWrapper = styled.div`
    display: flex;

    flex-direction: column;

    gap: 20px;
`;


const EmptyCard = styled.div`
    min-height: 300px;

    display: flex;

    align-items: center;
    justify-content: center;

    padding: 30px;

    border-radius: 24px;

    border: 1px solid
    rgba(
            255,
            255,
            255,
            0.08
    );

    background:
            rgba(
                    255,
                    255,
                    255,
                    0.04
            );

    color: #707785;
`;


const AnalysisCard = styled.div`
    padding: 26px;

    border-radius: 20px;

    background: #151a23;

    border: 1px solid
    rgba(
            255,
            255,
            255,
            0.08
    );
`;


const SectionLabel = styled.div`
    margin-bottom: 8px;

    font-size: 12px;
    font-weight: 700;

    letter-spacing: 1.3px;

    text-transform: uppercase;

    color: #8170ff;
`;


const AnalysisText = styled.p`
    margin: 0;

    white-space: pre-line;

    line-height: 1.8;

    color: #d7dbe3;
`;


const ResultHeader = styled.div`
    display: flex;

    justify-content:
            space-between;

    align-items:
            flex-end;
`;


const ResultTitle = styled.h2`
    margin: 0;

    color: white;
`;


const ResultGrid = styled.div`
    display: grid;

    grid-template-columns:
        repeat(
            2,
            minmax(
                    0,
                    1fr
            )
        );

    gap: 14px;

    @media (
        max-width: 850px
    ) {
        grid-template-columns:
            1fr;
    }
`;


const ResultCard = styled.div`
    position: relative;

    overflow: hidden;

    border-radius: 18px;

    background: #161c25;

    border: 1px solid
    rgba(
            255,
            255,
            255,
            0.07
    );

    transition: 0.2s;

    &:hover {
        transform:
                translateY(-3px);

        border-color:
                rgba(
                        124,
                        92,
                        255,
                        0.5
                );
    }
`;


/* =========================================
   S3 이미지
========================================= */

const ImageWrapper = styled.div`
    width: 100%;

    height: 210px;

    overflow: hidden;

    background: #0d1118;
`;


const ResultImage = styled.img`
    width: 100%;

    height: 100%;

    object-fit: cover;

    display: block;

    transition: transform 0.3s ease;

    ${ResultCard}:hover & {
        transform: scale(1.03);
    }
`;


/* =========================================
   카드 내용
========================================= */

const CardContent = styled.div`
    position: relative;

    padding: 22px;
`;


const Rank = styled.div`
    position: absolute;

    right: 18px;
    top: 18px;

    color: #8170ff;

    font-weight: 800;

    font-size: 19px;
`;


const FoodName = styled.div`
    padding-right: 50px;

    color: white;

    font-size: 21px;
    font-weight: 700;
`;


const Similarity = styled.div`
    margin-top: 15px;

    color: #8d96a5;

    strong {
        color: #82e6bc;
    }
`;


const Path = styled.div`
    margin-top: 15px;

    padding-top: 14px;

    border-top: 1px solid
    rgba(
            255,
            255,
            255,
            0.06
    );

    color: #606978;

    font-size: 11px;

    word-break: break-all;
`;