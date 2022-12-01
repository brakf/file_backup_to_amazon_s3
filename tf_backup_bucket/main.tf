resource "aws_s3_bucket" "this" {
  bucket_prefix = var.company_prefix
  # force_destroy = true
}

resource "aws_s3_bucket_versioning" "this" {
  bucket = aws_s3_bucket.this.id

   versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "this" {
  bucket = aws_s3_bucket.this.id
 rule {
    id = "delete-older-than-5-days"

    filter {}

    status = "Enabled"

    noncurrent_version_expiration{
      newer_noncurrent_versions = 5
      noncurrent_days = 5
    }
 }

 }

 

# resource "aws_s3_bucket_object_lock_configuration" "this" {
#   bucket = aws_s3_bucket.this.bucket

#   rule {
#     default_retention {
#       mode = "GOVERNANCE"
#       days = 5
#     }
#   }
# }

output "bucket_name" {
 value = aws_s3_bucket.this.id 
}

resource "aws_s3_bucket_server_side_encryption_configuration" "this" {
  bucket = aws_s3_bucket.this.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}