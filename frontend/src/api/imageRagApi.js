import api from "./client";


export async function searchImageRag(
    file,
    topK = 5,
) {
    const formData = new FormData();

    formData.append(
        "file",
        file,
    );

    const response = await api.post(
        "/image-rag/search",
        formData,
        {
            params: {
                top_k: topK,
            },
        },
    );

    return response.data;
}