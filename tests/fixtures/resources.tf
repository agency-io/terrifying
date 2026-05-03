resource "aws_s3_bucket" "bucket_one" {
  bucket = var.bucket_name
}

resource "aws_s3_bucket" "bucket_two" {
  bucket = var.other_bucket
}
