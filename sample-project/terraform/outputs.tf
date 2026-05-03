output "instance_id" {
  description = "ID of the web EC2 instance"
  value       = aws_instance.web.id
}

output "bucket_name" {
  value = aws_s3_bucket.data.bucket
}
