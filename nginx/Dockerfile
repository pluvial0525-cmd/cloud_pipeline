# =========================================================
# Stage 1
# React Build
# =========================================================

FROM node:24-alpine AS frontend-build


WORKDIR /frontend


# package 파일 먼저 복사
COPY frontend/package*.json ./


# npm 패키지 설치
RUN npm ci


# frontend 전체 복사
COPY frontend/ .


# React build
RUN npm run build



# =========================================================
# Stage 2
# Nginx
# =========================================================

FROM nginx:alpine


# 기본 nginx 설정 제거
RUN rm /etc/nginx/conf.d/default.conf


# 사용자 nginx 설정
COPY nginx/nginx.conf \
    /etc/nginx/conf.d/default.conf


# React build 결과 복사
COPY --from=frontend-build \
    /frontend/dist \
    /usr/share/nginx/html


EXPOSE 80


CMD [
    "nginx",
    "-g",
    "daemon off;"
]