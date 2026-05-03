variable "environment" {
  description = "Deployment environment (prod, staging, dev)"
  type        = string
  default     = "dev"
}

variable "instance_type" {
  type    = string
  default = "t2.micro"
}

variable "team" {
  description = "Owning team name"
  type        = string
}
