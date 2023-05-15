# Exercise 02

## Goal

You will try to read a file in an S3 bucket owned by someone else and learn about IAM permissions along the way.

## Instructions

### Step 1 - Try to Read the Bucket

> **NOTE**: Replace ANOTHER_BUCKET_NAME with the bucket name the lecturer provides. This also works if you alter the command to download any file a teammate has uploaded to their bucket.

1. Try to download the file. It will fail.

```shell
aws s3api get-object --bucket ANOTHER_BUCKET_NAME --key fake_dir/wizeline_file.txt wizeline_file.txt
```

2. Read the ERROR that appears

```
# An error occurred (AccessDenied) when calling the GetObject operation: Access Denied
```

3. No Profit! T_T


### Step 2 - Get Read Permissions to the bucket

> **NOTE**: Replace ANOTHER_BUCKET_NAME with the bucket name the lecturer provides. This also works if you alter the command to download any file a teammate has uploaded to their bucket.

1. Get your ARN with the following command

```shell
aws sts get-caller-identity
```

2. Verify the output contains the following key values

```shell
{
    "UserId": "AIDASAMPLEUSERID",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/DevAdmin"
}
```

3. Share the value in the "Arn" key with the bucket owner
4. Wait for them to grant you permissions. Bucket Owners see instructions below.
5. Try to download the file again!

```shell
aws s3api get-object --bucket ANOTHER_BUCKET_NAME --key fake_dir/wizeline_file.txt wizeline_file.txt
```

6. Open the downloaded file

## Sharing your bucket with a list of ARNs

1. Get the ARNs with whom you want to share your bucket. They look like this.
  * E.g. "arn:aws:iam::123456789012:user/DevAdmin"
  * E.g. "arn:aws:iam::123456789012:user/DevAdmin2"
2. Get the ARN of your bucket. It looks like this
  * E.g. "arn:aws:s3:::deb-s12-resources"
3. Update the following JSON accordingly with the ARNs
  * The `/*` in one of the resources is to include all files in the bucket.
4. Copy the updated JSON
5. Open the AWS S3 service in the Web Console (https://s3.console.aws.amazon.com/s3/buckets?region=us-east-1)
6. Click your bucket name in the list
7. Navigate to the "Permissions" in the main panel
8. Scroll down to the "Bucket policy" section in the main panel. 
9. Click the "Edit" button on the right side of the "Bucket policy" section
10. Paste the JSON you copied
11. Click the orange "Save changes" button on the lower right


```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "",
            "Effect": "Allow",
            "Principal": {
                "AWS": [
                    "arn:aws:iam::123456789012:user/DevAdmin",
                    "arn:aws:iam::123456789012:user/DevAdmin2"
                ]
            },
            "Action": [
                "s3:ListBucket",
                "s3:GetObject",
                "s3:GetBucketLocation"
            ],
            "Resource": [
                "arn:aws:s3:::deb-s12-resources/*",
                "arn:aws:s3:::deb-s12-resources"
            ]
        }
    ]
}
```
