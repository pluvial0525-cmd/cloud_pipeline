pipeline {

    agent any


    // =====================================================
    // Environment
    // =====================================================

    environment {

        APP_NAME = "ksm_project"

        AWS_HOST = "15.165.43.54"

        AWS_USER = "ubuntu"

        DEPLOY_PATH = "/home/ubuntu/ksm_project"

    }


    stages {


        // =================================================
        // 1. GitHub Checkout
        // =================================================

        stage("Checkout") {

            steps {

                echo "GitHub 프로젝트 가져오기"

                checkout scm

            }

        }


        // =================================================
        // 2. .env 생성
        // =================================================

        stage("Environment") {

            steps {

                echo ".env 설정"

                withCredentials([
                    file(
                        credentialsId: "ksm-env",
                        variable: "ENV_FILE"
                    )
                ]) {

                    sh '''
                        rm -f .env
                        cp "$ENV_FILE" .env
                        chmod 600 .env
                    '''

                }

            }

        }


        // =================================================
        // 3. Docker Build Test
        // =================================================

        stage("Docker Build") {

            steps {

                echo "Docker 이미지 Build 테스트"

                sh '''
                    docker-compose build
                '''

            }

        }


        // =================================================
        // 4. AWS EC2 전송
        // =================================================

        stage("Deploy Files") {

            steps {

                echo "AWS EC2로 프로젝트 전송"

                sshagent(
                    credentials: [
                        "aws-ec2-ssh"
                    ]
                ) {

                    sh """

                        ssh \
                        -o StrictHostKeyChecking=no \
                        ${AWS_USER}@${AWS_HOST} \
                        "mkdir -p ${DEPLOY_PATH}"


                        rsync \
                        -avz \
                        --delete \
                        --exclude='.git' \
                        --exclude='.idea' \
                        --exclude='.venv' \
                        --exclude='node_modules' \
                        --exclude='backend/images' \
                        ./ \
                        ${AWS_USER}@${AWS_HOST}:${DEPLOY_PATH}/

                    """

                }

            }

        }


        // =================================================
        // 5. AWS Docker Compose Deploy
        // =================================================

        stage("AWS Deploy") {

            steps {

                echo "AWS Docker Compose 배포"

                sshagent(
                    credentials: [
                        "aws-ec2-ssh"
                    ]
                ) {

                    sh """

                        ssh \
                        -o StrictHostKeyChecking=no \
                        ${AWS_USER}@${AWS_HOST} '

                            cd ${DEPLOY_PATH}

                            docker-compose down

                            docker-compose build

                            docker-compose up -d

                            docker image prune -f

                        '

                    """

                }

            }

        }


        // =================================================
        // 6. Container Check
        // =================================================

        stage("Health Check") {

            steps {

                echo "컨테이너 상태 확인"

                sshagent(
                    credentials: [
                        "aws-ec2-ssh"
                    ]
                ) {

                    sh """

                        ssh \
                        -o StrictHostKeyChecking=no \
                        ${AWS_USER}@${AWS_HOST} '

                            cd ${DEPLOY_PATH}

                            docker-compose ps

                        '

                    """

                }

            }

        }

    }


    // =====================================================
    // Pipeline 결과
    // =====================================================

    post {

        success {

            echo "===================================="
            echo "AWS 자동 배포 성공"
            echo "===================================="

        }


        failure {

            echo "===================================="
            echo "AWS 자동 배포 실패"
            echo "Jenkins Console Output 확인"
            echo "===================================="

        }

    }

}