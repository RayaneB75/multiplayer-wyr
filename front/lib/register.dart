import 'package:flutter/material.dart';
import 'package:frontend/findMatch.dart';
import 'package:frontend/items.dart';

class RegisterWindow extends StatelessWidget {
  const RegisterWindow({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        //title: const Text('Register'),
      ),
      body: const Center(
        child: RegisterForm()
      ),
    );
  }
}

class RegisterForm extends StatelessWidget {
  const RegisterForm({super.key});

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      crossAxisAlignment: CrossAxisAlignment.center,
      children: <Widget>[

        const Text(
          'Register',
          style: TextStyle(fontSize: 30),
        ),

        const SizedBox(height: 120),

        const TextFieldCustom(content: "Enter your IMT Atlantique email"),
        const TextFieldCustom(content: "Enter your password"),
        const TextFieldCustom(content: "Confirm your password"),

        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 16),
          child: ElevatedButton(
            onPressed: () {
             Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => const FindMatchWindow()),
                );
            },
            child: const Text('Register'),
          ),
        ),
      ],
    );
  }
}