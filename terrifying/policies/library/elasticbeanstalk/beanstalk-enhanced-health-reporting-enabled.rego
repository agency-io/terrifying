# title: beanstalk-enhanced-health-reporting-enabled
# description: Detects Elastic Beanstalk environments without enhanced health reporting enabled. Equivalent to AWS Config beanstalk-enhanced-health-reporting-enabled. Maps to FSBP ElasticBeanstalk.1 (Low).
# severity: Low
# tags: security-hub, fsbp
# terraform_resources: aws_elastic_beanstalk_environment
package terrifying

import rego.v1

deny contains msg if {
	resource := input.resources[_]
	resource.type == "aws_elastic_beanstalk_environment"
	not enhanced_health_reporting_enabled(resource)
	msg := sprintf("Resource %v.%v: Elastic Beanstalk environment does not have enhanced health reporting enabled", [resource.type, resource.name])
}

enhanced_health_reporting_enabled(resource) if {
	some setting in resource.attributes.setting
	setting.namespace == "aws:elasticbeanstalk:healthreporting:system"
	setting.name == "SystemType"
	setting.value == "enhanced"
}
