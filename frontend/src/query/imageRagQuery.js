import { useMutation } from "@tanstack/react-query";

import {
    searchImageRag,
} from "../api/imageRagApi";


export function useImageRagMutation() {
    return useMutation({
        mutationFn: ({
                         file,
                         topK,
                     }) =>
            searchImageRag(
                file,
                topK,
            ),
    });
}