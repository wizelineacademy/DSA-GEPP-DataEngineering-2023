# GEPP - QUESTION - What is that ${} syntax in lines 15 and 20?

# Create state machine for step function
resource "aws_sfn_state_machine" "sfn_state_machine" {
  name     = "deb-state-machine-by-${var.deb_student}"
  role_arn = "arn:aws:iam::908781576184:role/smontiel_iam_for_step_function"

  # GEPP - EXERCISE - Get the ARNs of 
  definition = <<EOF
{  
   "StartAt":"Step1__Run_Load_Lambda",
   "States":{  
      "Step1__Run_Load_Lambda":{  
         "Type":"Task",
         "Resource":"${aws_lambda_function.load_lambda.arn}",
         "Next":"Step2__Run_Transform_Lambda"
      },
      "Step2__Run_Transform_Lambda":{  
         "Type":"Task",
         "Resource":"${aws_lambda_function.transform_lambda.arn}",
         "End":true
      }
   }
}
EOF

}
