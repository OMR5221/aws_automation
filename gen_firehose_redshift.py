from troposphere import Template, Output, Ref
from troposphere.s3 import Bucket, PublicRead
from troposphere.firehose import (
    BufferingHints,
    CloudWatchLoggingOptions,
    CopyCommand,
    DeliveryStream,
    EncryptionConfiguration,
    KMSEncryptionConfig,
    RedshiftDestinationConfiguration,
    S3Configuration,
)


t = Template()
t.add_version('2010-09-09')
t.add_description('Sample Kinesis Firehose Delivery Stream')


t.add_resource(DeliveryStream(
    'TestDeliveryStream',
    DeliveryStreamName='TestDeliveryStream',
    RedshiftDestinationConfiguration=RedshiftDestinationConfiguration(
        CloudWatchLoggingOptions=CloudWatchLoggingOptions(
            Enabled=True,
            LogGroupName='my-log-group',
            LogStreamName='my-log-stream',
        ),
        # Connection string Kinesis Data Firehose uses to connect to the Redshift cluster:
        # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-redshiftdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-redshiftdestinationconfiguration-clusterjdbcurl
        ClusterJDBCURL='jdbc:redshift://my-redshift-db.asdf.us-west-2.redshift.amazonaws.com:5432/mydb', # noqa
        # Configures the Redshift copy command Firehose will use to load the data into the cluster
        # from the S3 bucket:
        CopyCommand=CopyCommand(
            CopyOptions="JSON 'auto'",
            DataTableColumns='mycol',
            DataTableName='mytable',
        ),
        # Password o the Redshift user specified in Username property
        Password='',
        # ARN of the AWS Identity  and Access Management (IAM) role that grants Firehose access to
        # your S3 bucket
        RoleARN='arn:aws:iam::12345:role/my-role',
        # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-s3destinationconfiguration.html
        S3Configuration=S3Configuration(
            BucketARN='arn:aws:s3::my-bucket',
            BufferingHints=BufferingHints(
                IntervalInSeconds=5,
                SizeInMBs=60,
            ),
            CloudWatchLoggingOptions=CloudWatchLoggingOptions(
                Enabled=True,
                LogGroupName='my-other-log-group',
                LogStreamName='my-other-log-stream',
            ),
            CompressionFormat='UNCOMPRESSED',
            EncryptionConfiguration=EncryptionConfiguration(
                KMSEncryptionConfig=KMSEncryptionConfig(
                    AWSKMSKeyARN='aws-kms-key-arn'
                ),
                NoEncryptionConfig='NoEncryption',
            ),
            Prefix='my-prefix',
            RoleARN='arn:aws:iam::12345:role/my-role',
        ),
        Username='omr',
    )
))

print(t.to_json())
