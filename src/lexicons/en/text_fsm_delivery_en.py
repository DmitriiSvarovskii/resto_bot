delivery_fsm_text: dict[str, str] = {
    'delivery_districts': 'To place a delivery order, please answer a few '
                          'questions, just a couple of minutes.\n\n'
                          'Select the district where you need '
                          'the order to be delivered.',
    'abort_delivery': 'You have aborted the delivery process.\n\n',
    'order_saved_message': 'Your order is still saved in the cart, '
                           'you can continue the process at '
                           'any time convenient for you.',
    'phone_input': 'Now, please enter your local (Indian) phone number '
                   'in the format "7812345678", without +91.'
                   "If you don't have a local phone number, "
                   'click "Skip step"',
    'phone_number_error_message': 'It seems there is an error in the phone '
                                  'number, please check the correctness '
                                  'of the number.\n\n'
                                  'The phone number should consist of '
                                  '10 digits.\n\n'
                                  'If you do not have a local number, click '
                                  'the "Skip step" button',
    'delivery_comment_prompt': "Okay, let's move on.\n\n"
                               'Now write a comment for the courier.\n\n'
                               'If there are no comments, click "Skip step")',
    'location_request_step': "Great, just one more step and we're done))\n\n"
                             'Now send us your location\n\n'
                             'IMPORTANT. To attach your location, use the '
                             'Telegram location sending feature.\n\n'
                             'If you are unable to send your location, click '
                             '"Skip step" and contact our manager for '
                             'further details @AyratZiganshin59',
    'error_comment': 'Some error occurred..\n\n'
                     'Please repeat the comment for the courier\n\n'
                     'Or click "Skip step"',
    'error_location': "What you sent doesn't seem like a location\n\n"
                      'Please make sure you are attaching '
                      'your location properly\n\n'
                      'If you want to cancel the form filling - '
                      'click on the "Cancel order ❌" button',
    'done_fsm_delivery': 'To confirm the order, press the button.',
    'use_buttons_for_districts': 'Please use the buttons when selecting the '
                                 'district.\n\nIf you want to cancel '
                                 'the delivery process - '
                                 'click on the "Cancel order ❌" button',
    'skip': 'Skip step',
    'good': 'Great!\n\n',
    'not_specified': 'Not specified',
    'send_location': 'Send location ✅',
    'confirm_delivery': 'Confirm delivery 🚚',

}
