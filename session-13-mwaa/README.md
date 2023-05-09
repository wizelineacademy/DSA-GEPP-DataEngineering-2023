# Wizeline Academy DSA-GEPP DataEngineering Bootcamp 2023

## Infrastructure as Code

### Session 13

### TOPICS

- Código en Terraform para la creación de un ambiente de MWAA con un bucket de S3, grupos de seguridad y rol IAM
- Crea una nueva VPC de muestra, 2 subredes privadas y 2 subredes públicas
- Crea una puerta de enlace de Internet para subredes públicas y una puerta de enlace NAT para subredes privadas
- Variables: Uso de variables a traves de los recursos y modulos
- Modules: Uso de Modulos


### Prerequisites:
Asegúrese de haber instalado las siguientes herramientas en su computadora portátil Mac o Windows antes de comenzar a trabajar con este módulo y ejecutar Terraform Plan and Apply

1. [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
2. [Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli)

### Deployment Steps

```sh
git clone https://github.com/wizelineacademy/DSA-GEPP-DataEngineering-2023
```

#### Step 2: Run Terraform INIT

```sh
terraform init
```

#### Step 3: Run Terraform PLAN

```sh
export AWS_REGION=<ENTER YOUR REGION>   # default set to `us-east-1`
terraform plan
```

#### Step 4: Finally, Terraform APPLY

```sh
terraform apply
```


#### Step 5: Verify the Amazon MWAA with login

La salida de la aplicación Terraform debería ser similar a

```
Changes to Outputs:
  + mwaa_arn               = "arn:aws:airflow:us-west-2:1234567897:environment/basic-mwaa"
  + mwaa_role_arn          = "arn:aws:iam::1234567897:role/mwaa-executor20220627111648219100000002"
  + mwaa_security_group_id = "sg-080b8fd440147d816"
  + mwaa_service_role_arn  = "arn:aws:iam::1234567897:role/aws-service-role/airflow.amazonaws.com/AWSServiceRoleForAmazonMWAA"
  + mwaa_status            = "AVAILABLE"
  + mwaa_webserver_url     = "b193b9bb-03d7-4086-ad83-c4e6ab5a023a.c24.us-west-2.airflow.amazonaws.com"
```

Abra la URL (`mwaa_webserver_url`) desde un navegador para verificar Amazon MWAA

#### Step 6: Verify the Amazon MWAA using the sample Apache Airflow workflow

En la carpeta `dags` tendrá un archivo DAG simple (`hello_world_dag.py`) que puede usar para probar su entorno MWAA.
Este es un flujo de trabajo muy simple que tiene dos tareas que usan BashOperator para hacer echo de una cadena simple.

**Terraform generated S3 bucket**

Copie este archivo utilizando la CLI de AWS con el siguiente comando, reemplazando `{mwaa_dags_folder}` con el nombre del depósito S3 de su entorno MWAA.

```sh
cd dags
aws s3 cp hello_world_dag.py s3://{mwaa_dags_folder}/dags/
```

**Bring your own S3 Bucket**

Si proporcionó un ARN de depósito de S3 para usar durante la configuración del entorno MWAA, use el siguiente comando para copiar el dag de muestra.

```sh
cd dags
aws s3 cp hello_world_dag.py s3://{your_s3_bucket}/dags/
```

Una vez que se haya copiado el DAG, pueden pasar de 2 a 3 minutos antes de que aparezca el DAG en la interfaz de usuario de Apache Airflow.

<p align="center">
  <img src="https://raw.githubusercontent.com/aws-ia/terraform-aws-mwaa/main/images/mwaa-dag-ui.png" alt="example DAGs in Apache Airflow UI" width="100%">
</p>

De manera predeterminada, estará deshabilitado (en pausa), pero puede habilitarlo y luego debería ejecutarse.

<p align="center">
  <img src="https://raw.githubusercontent.com/aws-ia/terraform-aws-mwaa/main/images/mwaa-dag-running.png" alt="viewing the DAG running" width="100%">
</p>

Verifique el estado de la tarea y vea los registros para asegurarse de obtener el resultado esperado.

<p align="center">
  <img src="https://raw.githubusercontent.com/aws-ia/terraform-aws-mwaa/main/images/mwaa-example-log.png" alt="viewing the DAG log files in Apache Airflow UI" width="100%">
</p>

Además, puede consultar los registros de CloudWatch del entorno MWAA para asegurarse de que se hayan creado todos y que pueda ver el resultado generado como parte de este flujo de trabajo.

<p align="center">
  <img src="https://raw.githubusercontent.com/aws-ia/terraform-aws-mwaa/main/images/mwaa-cloudwatch-loggroup.png" alt="look at the CloudWatch log groups created" width="100%">
</p>

## Cleanup
Para limpiar su entorno, destruya el módulo de terraform.

*NOTE:* Vacíe el bucket S3 creado por este módulo antes de ejecutar el `terraform destroy`

```sh
terraform destroy -auto-approve
```
