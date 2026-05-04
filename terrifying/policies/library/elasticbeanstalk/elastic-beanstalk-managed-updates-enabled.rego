# title: elastic-beanstalk-managed-updates-enabled
# description: Detects Elastic Beanstalk environments with managed updates disabled. Equivalent to AWS Config elastic-beanstalk-managed-updates-enabled. Maps to FSBP ElasticBeanstalk.2 (High).
# severity: High
# tags: security-hub, fsbp
# terraform_resources: aws_elastic_beanstalk_environment
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_elastic_beanstalk_environment"
	not managed_updates_enabled(resource)
	msg := sprintf("Resource %v.%v: Elastic Beanstalk environment does not have managed updates enabled", [resource.type, resource.name])
}

managed_updates_enabled(resource) if {
	some setting in resource.attributes.setting
	setting.namespace == "aws:elasticbeanstalk:managedactions"
	setting.name == "ManagedActionsEnabled"
	setting.value == "true"
}
