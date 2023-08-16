import 'package:flutter/material.dart';
import 'package:frontend/api_calls.dart';
import 'package:frontend/register.dart';
import 'package:frontend/login.dart';

void main() {
  runApp( MaterialApp(
    title: 'Would You Rather',
    home: const Home(),
    theme: ThemeData.dark(
        useMaterial3: true,
        ),
  ));
}

class Home extends StatelessWidget {
  const Home({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        //title: const Text('Would you rather ...'),
      ),
      body: Center(
        child: Column(
          mainAxisSize: MainAxisSize.max,
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            const Text(
              'Would you rather ...',
              style: TextStyle(fontSize: 20),
            ),
            const SizedBox(height: 50),
            ElevatedButton(
              child: const Text('Register'),
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => const RegisterWindow()),
                );
              },
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              child: const Text('Login'),
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => const LoginWindow()),
                );
              },
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              child: const Text('TEST API CALL'),
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => const TestApi()),
                );
              },
            ),
          ],
        ),
        
      ),
    );
  }
}