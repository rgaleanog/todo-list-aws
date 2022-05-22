# todo-list-aws

Este proyecto contiene un ejemplo de solución **SAM + Jenkins**. Contiene una aplicación API RESTful de libreta de tareas pendientes (ToDo) y los pipelines que permiten definir el CI/CD para productivizarla.

## ESTRUCTURA

A continuación se describe la estructura del proyecto:
- **pipelines** - pipelines de Jenkins que permiten construir el CI/CD
- **src** - en este directorio se almacena el código fuente de las funciones lambda con las que se va a trabajar
- **test** - Tests unitarios y de integración. 
- **samconfig.toml** - Configuración de los stacks de Staging y Producción
- **template.yaml** - Template que define los recursos AWS de la aplicación
- **localEnvironment.json** - Permite el despliegue en local de la aplicación sobreescribiendo el endpoint de dynamodb para que apunte contra el docker de dynamo

## DESPLIEGUE manual de la aplicación SAM en AWS

Para utilizar SAM CLI se necesitan las siguientes herramientas:

* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3 installed](https://www.python.org/downloads/) - Se ha testeado con Python 3.7
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

### Para **construir** la aplicación se deberá ejecutar el siguiente comando:
```bash
sam build
```
### DESPLEGAR la aplicación por primera vez:

Sin utilizar la configuración del archivo samconfig.toml. Se generará un archivo de configuración reemplazando al actual si ya existe.
Ejecutar el siguiente comando:
```bash
sam deploy --guided
```

El despliegue de la aplicación empaqueta, publicará en un bucket s3 el artefacto y desplegará la aplicación en AWS. Solicitará la siguiente información

* **Stack Name**: El nombre del stack que desplegará en CloudFormation. Debe ser único
* **AWS Region**: La región en la que se desea publicar la Aplicación.
* **Confirm changes before deploy**: Si se indica "yes" se solicitará confirmación antes del despliegue si se encuentran cambios 
* **Allow SAM CLI IAM role creation**: Permite la creación de roles IAM
* **Save arguments to samconfig.toml**: Si se selecciona "yes" las respuestas se almacenarán en el fichero de configuración samconfig.toml, de esta forma el el futuro se podrá ejecutar con `sam deploy` y se leerá la configuración del fichero.

En el output del despliegue se devolverá el API Gateway Endpoint URL

### DESPLEGAR la aplicación con la configuración de **samconfig.toml**:
Revisar el fichero samconfig.toml
```bash
vim samconfig.toml
```
Buscar en la configuración los buckets donde se van a almacenar los artefactos y modificar el fichero para que apunte al bucket del alumno, para ello hay que modificar las XXXXXX por otro nombre identificativo. Previamente se deberá crear los buckets a través de la consola de AWS!!!
```bash
s3_bucket = "aws-sam-cli-managed-staging-samclisourcebucket-XXXXXX" #Incluir bucket propio. Previamente se deberá crear los buckets a través de la consola de AWS!!!
```
```bash
s3_bucket = "aws-sam-cli-managed-production-samclisourcebucket-XXXXXX" #Incluir bucket propio. Previamente se deberá crear los buckets a través de la consola de AWS!!!
```
Ejecutar el siguiente comando para el entorno de **default**. Nota: usar este para pruebas manuales y dejar el resto para los despliegues con Jenkins.
```bash
sam deploy template.yaml --config-env default
```
Ejecutar el siguiente comando para el entorno de **staging**
```bash
sam deploy template.yaml --config-env staging
```
Ejecutar el siguiente comando para el entorno de **producción**
```bash
sam deploy template.yaml --config-env prod
```

## DESPLIEGUE manual de la aplicación SAM en local

A continuación se describen los comandos/acciones a realizar para poder probar la aplicación en local:
```bash
## Crear red de docker
docker network create sam

## Levantar el contenedor de dynamodb en la red de sam con el nombre de dynamodb
docker run -p 8000:8000 --network sam --name dynamodb -d amazon/dynamodb-local

## Crear la tabla en local, para poder trabajar localmemte
aws dynamodb create-table --table-name local-TodosDynamoDbTable --attribute-definitions AttributeName=id,AttributeType=S --key-schema AttributeName=id,KeyType=HASH --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1 --endpoint-url http://localhost:8000

## Empaquetar sam
sam build # también se puede usar sam build --use-container si se dan problemas con las librerías de python

## Levantar la api en local, en el puerto 8080, dentro de la red de docker sam
sam local start-api --port 8081 --env-vars localEnvironment.json --docker-network sam
```

## CONSULTAR logs de las funciones lambda

Se pueden consultar en CloudWath o ejecutando un comando similar al siguiente:
```bash
sam logs -n GetTodoFunction --stack-name todo-list-aws-staging
```

## Tests

Se encuentran en la carpeta `test` que tiene la siguiente estructura:
```
- test
|--- integration (tests de integración)
|       -- todoApiTest.py
|--- unit (tests unitarios)
|       -- TestToDo.py
```
Para ejecutar los tests de **integración** es necesario ejecutar los siguientes comandos:
```bash
python -m pip install pytest
python -m pip install requests
pytest -s test/integration/todoApiTest.py
```

Para ejecutar los tests **unitarios** es necesario ejecutar los siguientes comandos:
```bash
python3.7 -m venv pyenvunittests
source pyenvunittests/bin/activate
python3.7 -m pip install --upgrade pip
python3.7 -m pip install boto3
python3.7 -m pip install moto
python3.7 -m pip install mock==4.0.2
python3.7 -m pip install coverage==4.5.4
export PYTHONPATH="${PYTHONPATH}:<directorio de la aplicación>"
export DYNAMODB_TABLE=todoUnitTestsTable
python test/unit/TestToDo.py
```
Otra alternativa es ejecutar los test desde la raíz del proyecto invocando a los scripts alojados dentro de la carpeta pipelines:
```bash
# Ejecución Pruebas

## Configuración del entorno virtual
pipelines/PIPELINE-FULL-STAGING/setup.sh

## Pruebas unitarias
pipelines/PIPELINE-FULL-STAGING/unit_test.sh

## pruebas estáticas (seguridad, calidad, complejidad )
pipelines/PIPELINE-FULL-STAGING/static_test.sh

# Pruebas de integración
pipelines/common-steps/integration.sh
```

## PIPELINES

Para la implementación del CI/CD de la aplicación se utilizan los siguientes Pipelines:
*	**PIPELINE-FULL-STAGING**: (PIPELINE-FULL-STAGING/Jenkinsfile) Este pipeline es el encargado de configurar el entorno de staging y ejecutar las pruebas
*	**PIPELINE-FULL-PRODUCTION**: (PIPELINE-FULL-PRODUCTION/Jenkinsfile) Este pipeline es el encargado de configurar el entorno de production y ejecutar las pruebas
*	**PIPELINE-FULL-CD**: este pipeline es el encargado de enganchar los pipelines de staging y production,  con el objetivo de completar un ciclo de despliegue continuo desde un commit al repositorio de manera automática.


## Limpieza

Para borrar la apliación y eliminar los stacks creados ejecutar los siguientes comandos:

```bash
aws cloudformation delete-stack --stack-name todo-list-aws-staging
aws cloudformation delete-stack --stack-name todo-list-aws-production
```

