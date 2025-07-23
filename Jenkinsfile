pipeline {
    agent any

    environment {
        PATH = "${PATH}:${HOME}/.local/bin"
    }

    stages {
        stage('Cloning Apache Airflow repo the repo') {
            steps {
                git branch: 'ApacheAirflowPipelinw', url: 'https://github.com/Bazla24/Ace-Surveillance.git'
                // print all the files in the repo and use bat
                bat 'dir'
            }
        }

        // add a stage cloning dvc repo
        stage('Cloning DVC repo') {
            steps {
            
                dir('examples/intro-example/dags') {
                    // clone the dvc repo
                    git branch: 'DVC', url: 'https://github.com/Bazla24/Ace-Surveillance.git'
                    // print all the files in the repo and use bat
                    

                    // go in dvc folder and print all the files
                    dir('dvc') {
                        bat 'dir'
                    }
                        
                        // run command dvc pull
                    //     bat 'dvc pull'
                    //     dir ('data') {
                    //         bat 'dir'
                    //     }
                    // }
                }

            }
        }
        

        // cloning mlFlow branch in examples/intro-example/dags
        stage('Cloning mlFlow repo') {
            steps {
                dir('examples/intro-example/dags/models') {
                    // clone the dvc repo
                    git branch: 'mlFlow', url: 'https://github.com/Bazla24/Ace-Surveillance.git'
                    // print all the files in the repo and use bat
                    bat 'dir'
                }
            }
        }

        stage('Running Airflow') {
            steps {
                // print all the files in the repo and use bat
                bat 'docker-compose up -d'
            }
        }
        

        

        

    }
}
