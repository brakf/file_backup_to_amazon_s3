resource "aws_iam_user" "backup_user" {
  name = var.user_name



}
resource "aws_iam_access_key" "backup_user" {
  user = aws_iam_user.backup_user.name
}

output "aws_iam_access_key" {
  value     = "${aws_iam_access_key.backup_user.id} | ${aws_iam_access_key.backup_user.secret}"
  sensitive = true
}


resource "aws_iam_user_policy" "backup_s3" {
  #   name = "test"
  name_prefix = var.company_prefix
  user        = aws_iam_user.backup_user.name


  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "s3:Put*",
        ]
        Effect   = "Allow"
        Resource = ["${aws_s3_bucket.this.arn}/*", "${aws_s3_bucket.this.arn}"]
      },
    ]
  })
}
