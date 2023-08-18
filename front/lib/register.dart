import 'package:flutter/material.dart';
import 'package:frontend/findMatch.dart';
import 'package:frontend/items.dart';
import 'package:frontend/login.dart';

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
      body: const Center(
        child: RegisterForm()
      ),
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
          TextFieldCustom(
            controller: passwordController,
            content: "Entre ton mot de passe",
            ),
          TextFieldCustom(
            controller: passwordCheckController,
            content: "Confirme ton mot de passe",
            ),
    
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 16),
            child: ElevatedButton(
              onPressed: () {
                if (_formKey.currentState!.validate()) {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => const LoginWindow()),
                  );
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