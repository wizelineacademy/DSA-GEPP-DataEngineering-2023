# Exercise 01

## Goal

> **NOTE**: This guide assumes you're working with a Windows OS.

You will setup the AWS CLI in your local Terminal (or equivalent). You will also create an S3 Bucket, Upload a File, Delete a File and Delete the bucket

## Instructions

### Step 1 - Install the AWS CLI

1. Download the [installer file](https://awscli.amazonaws.com/AWSCLIV2.msi ) for Windows
2. Execute the installer.
3. Open Terminal
  * Click the `Start` button. This will pop-up the Windows Start menu.
  * Type `cmd`. This will filter the on-screen menu.
  * Hit `Enter` in your keyboard. The Terminal screen will appear.

> NOTE: By default in Windows, the terminal screen is black with white letters.

4. Confirm installation
  * Type `aws --version`
  * Hit `Enter` in your keyboard. A message similar to the following should appear
  
> ```shell
> aws --version
> # aws-cli/2.8.12 Python/3.9.11 Darwin/21.5.0 exe/x86_64 prompt/off
> ```

5. Profit!

### Step 2 - Get your AWS Token

1. Open AWS IAM Console  in the Search Bar at the top of the page.
2. Navigate to "Users" in the left-side panel
3. Click your OWN IAM user name. It should match your login info.
4. Navigate to "Security Credentials" in the main panel
5. Click "Create access key" in the right side of the main panel
6. Click the "Show" button to temporarily display the credentials
7. Verify your credentials look like the below example
  * **Access key ID**: `AKIAIOSFODNN7EXAMPLE`
  * **Secret access key**: `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`
8. Open the Terminal
9. Execute the `aws configure` command
10. Profit!

### Step 3 - Interact with S3

> **NOTE**: Replace YOUR_BUCKET_NAME with any name you choose. Check the [S3 naming rules](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html).

1. Create S3 bucket with the following command

> ```shell
> aws s3api create-bucket --region us-east-1 --bucket YOUR_BUCKET_NAME
> 
> # EXAMPLE: aws s3api create-bucket --region us-east-1 --bucket my-unique-s3-bucket-name
> ```

2. Find your sample CSV file. If not found, create one of your own
  * It should be named `fake_data.csv`
  
3. Upload the file to the S3 bucket you created with the following command

> ```shell
> aws s3api put-object --bucket YOUR_BUCKET_NAME --key fakedir/fake_data.csv --body fake_data.csv
> ```

4. Download the remote file with the following command

> ```shell
> aws s3api get-object --bucket YOUR_BUCKET_NAME --key fakedir/fake_data.csv my_downloaded_file.csv
> ```

5. Delete the remote file you uploaded with the following command

> ```shell
> aws s3api delete-object --bucket YOUR_BUCKET_NAME --region us-east-1 --key fakedir/fake_data.csv
> ```

or

```shell
# This command deletes everything in the bucket recursively.
# Only works if Versioning is disabled
aws s3 rm s3://YOUR_BUCKET_NAME --recursive
```

6. Delete the bucket you created with the following command

> ```shell
> aws s3api delete-bucket --bucket YOUR_BUCKET_NAME --region us-east-1
> ```

7. Profit!