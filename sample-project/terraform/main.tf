resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"

  tags = {
    Environment = "prod"
    Team        = "platform"
  }
}

resource "aws_s3_bucket" "data" {
  bucket = "my-hardcoded-bucket-name"

  tags = {
    Environment = "prod"
  }
}
