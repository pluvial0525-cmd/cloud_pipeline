# =========================================================
# 1. React Build
# =========================================================

FROM node:24-alpine AS frontend-build

WORKDIR /app

COPY frontend/package*.json ./

RUN npm install

COPY frontend/ ./

RUN npm run build


# =========================================================
# 2. Nginx
# =========================================================

FROM nginx:alpine

# 기본 nginx 설정 제거
RUN rm /etc/nginx/conf.d/default.conf

# 우리가 만든 nginx 설정 복사
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf

# React 빌드 결과 복사
COPY --from=frontend-build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]