# title: sagemaker-notebook-instance-inside-vpc
# description: Detects SageMaker notebook instances not launched inside a custom VPC. Equivalent to AWS Config sagemaker-notebook-instance-inside-vpc.
# severity: High
# tags: security-hub, fsbp
# terraform_resources: aws_sagemaker_notebook_instance
package terrifying

import rego.v1

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_sagemaker_notebook_instance"
    not resource.attributes.subnet_id
    msg := sprintf("Resource %v.%v: SageMaker notebook instance is not inside a VPC", [resource.type, resource.name])
}
