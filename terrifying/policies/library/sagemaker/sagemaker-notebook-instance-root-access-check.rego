# title: sagemaker-notebook-instance-root-access-check
# description: Detects SageMaker notebook instances with root access enabled. Equivalent to AWS Config sagemaker-notebook-instance-root-access-check.
# severity: High
# tags: security-hub, fsbp
# terraform_resources: aws_sagemaker_notebook_instance
package terrifying

import rego.v1

deny contains msg if {
    resource := input.resources[_]
    resource.type == "aws_sagemaker_notebook_instance"
    resource.attributes.root_access == "Enabled"
    msg := sprintf("Resource %v.%v: SageMaker notebook instance has root access enabled", [resource.type, resource.name])
}
