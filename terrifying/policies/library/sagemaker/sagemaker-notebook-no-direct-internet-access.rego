# title: sagemaker-notebook-no-direct-internet-access
# description: Detects SageMaker notebook instances with direct internet access enabled. Equivalent to AWS Config sagemaker-notebook-no-direct-internet-access.
# severity: High
# tags: control-tower, security-hub, fsbp
# terraform_resources: aws_sagemaker_notebook_instance
package terrifying

import rego.v1

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_sagemaker_notebook_instance"
    resource.attributes.direct_internet_access == "Enabled"
    msg := sprintf("Resource %v.%v: SageMaker notebook instance has direct internet access enabled", [resource.type, resource.name])
}
