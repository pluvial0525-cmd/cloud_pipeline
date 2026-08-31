import { useEffect, useState } from "react";

import styled from "styled-components";


function ImageUpload({
                         onSearch,
                         isPending,
                     }) {
    const [file, setFile] =
        useState(null);

    const [preview, setPreview] =
        useState(null);


    useEffect(() => {
        if (!file) {
            setPreview(null);

            return;
        }

        const imageUrl =
            URL.createObjectURL(file);

        setPreview(imageUrl);


        return () => {
            URL.revokeObjectURL(
                imageUrl,
            );
        };
    }, [file]);


    const handleFileChange = (
        event,
    ) => {
        const selectedFile =
            event.target.files?.[0];

        if (!selectedFile) {
            return;
        }

        if (
            !selectedFile.type.startsWith(
                "image/",
            )
        ) {
            alert(
                "이미지 파일을 선택해주세요.",
            );

            return;
        }

        setFile(selectedFile);
    };


    const handleSearch = () => {
        if (!file) {
            alert(
                "검색할 이미지를 선택해주세요.",
            );

            return;
        }

        onSearch(file);
    };


    return (
        <UploadCard>
            <Title>
                음식 이미지 업로드
            </Title>

            <Description>
                이미지를 업로드하면
                유사한 한국 음식을
                찾아드립니다.
            </Description>

            <UploadArea>
                {preview ? (
                    <PreviewImage
                        src={preview}
                        alt="업로드 이미지"
                    />
                ) : (
                    <Placeholder>
                        이미지를 선택해주세요
                    </Placeholder>
                )}
            </UploadArea>

            <ButtonRow>
                <FileLabel>
                    이미지 선택

                    <HiddenInput
                        type="file"
                        accept="image/*"
                        onChange={
                            handleFileChange
                        }
                    />
                </FileLabel>

                <SearchButton
                    onClick={
                        handleSearch
                    }
                    disabled={
                        isPending
                    }
                >
                    {isPending
                        ? "검색 중..."
                        : "Image RAG 검색"}
                </SearchButton>
            </ButtonRow>
        </UploadCard>
    );
}


export default ImageUpload;


const UploadCard = styled.div`
    width: 100%;
    padding: 32px;

    border-radius: 24px;

    background:
            rgba(
                    255,
                    255,
                    255,
                    0.06
            );

    border: 1px solid
    rgba(
            255,
            255,
            255,
            0.1
    );
`;


const Title = styled.h2`
    margin: 0 0 10px;

    font-size: 26px;

    color: white;
`;


const Description = styled.p`
    margin: 0 0 24px;

    color: #aeb4c0;

    line-height: 1.6;
`;


const UploadArea = styled.div`
    width: 100%;
    height: 340px;

    display: flex;

    align-items: center;
    justify-content: center;

    overflow: hidden;

    border-radius: 18px;

    border: 1px dashed
    rgba(
            255,
            255,
            255,
            0.2
    );

    background: #11151c;
`;


const PreviewImage = styled.img`
    width: 100%;
    height: 100%;

    object-fit: contain;
`;


const Placeholder = styled.div`
    color: #777f8d;

    font-size: 15px;
`;


const ButtonRow = styled.div`
    display: flex;

    gap: 12px;

    margin-top: 20px;
`;


const FileLabel = styled.label`
    flex: 1;

    padding: 14px 18px;

    text-align: center;

    border-radius: 12px;

    background: #252b36;

    color: white;

    cursor: pointer;

    transition: 0.2s;

    &:hover {
        background: #313846;
    }
`;


const HiddenInput = styled.input`
    display: none;
`;


const SearchButton = styled.button`
    flex: 1;

    padding: 14px 18px;

    border: none;
    border-radius: 12px;

    background:
            linear-gradient(
                    135deg,
                    #7c5cff,
                    #5f8cff
            );

    color: white;

    font-size: 15px;
    font-weight: 700;

    cursor: pointer;

    transition: 0.2s;

    &:hover {
        transform:
                translateY(-1px);
    }

    &:disabled {
        opacity: 0.5;

        cursor: not-allowed;

        transform: none;
    }
`;