import 'package:flutter/material.dart';
import 'package:frontend/api_calls.dart';
import 'package:frontend/items.dart';

class RegisterWindow extends StatelessWidget {
  const RegisterWindow({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Image.asset(
          'assets/logo_resel.png',
          fit: BoxFit.contain,
          height: 32,
        ),
      ),
      body: const Center(child: RegisterForm()),
    );
  }
}

class RegisterForm extends StatefulWidget {
  const RegisterForm({super.key});

  @override
  State<RegisterForm> createState() => _RegisterFormState();
}

class _RegisterFormState extends State<RegisterForm> {
  final _formKey = GlobalKey<FormState>();

  final emailController = TextEditingController();
  final passwordController = TextEditingController();
  final passwordCheckController = TextEditingController();

  @override
  void dispose() {
    // Clean up the controller when the widget is disposed.
    emailController.dispose();
    passwordController.dispose();
    passwordCheckController.dispose();

    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Form(
      key: _formKey,
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: <Widget>[
          const Text(
            'S\'enregistrer',
            style: TextStyle(fontSize: 30),
          ),
          const SizedBox(height: 120),
          TextFieldCustom(
            controller: emailController,
            content: "Entre ton e-mail IMT Atlantique",
          ),
          PasswordFieldCustom(
            controller: passwordController,
            content: "Entre ton mot de passe",
          ),
          PasswordFieldCustom(
            controller: passwordCheckController,
            content: "Confirme ton mot de passe",
          ),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 16),
            child: ElevatedButton(
              onPressed: () {
                if (_formKey.currentState!.validate() &&
                    passwordController.text == passwordCheckController.text) {
                  // add message when password are not the same
                  ApiCalls.register(
                      emailController.text, passwordController.text, context);
                }
              },
              child: const Text('S\'enregistrer'),
            ),
          ),
        ],
      ),
    );
  }
}
