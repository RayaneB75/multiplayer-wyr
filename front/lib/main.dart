import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:simple_gradient_text/simple_gradient_text.dart';
import 'package:universal_html/html.dart' as html;

import 'package:flutter/material.dart';
import 'package:frontend/api_calls.dart';
import 'package:frontend/register.dart';
import 'package:frontend/login.dart';

void main() async {
  runApp(const Main());

  final splash = html.querySelector('#splash');
  if (splash != null) {
    await ApiCalls.openSession();
    splash.remove();
  }
}

class Main extends StatelessWidget {
  const Main({super.key});

  // Check if the user is connected, if not,
  // redirect to the login page

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Tu préfères ? by ResEl',
      home: const MainPage(),
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: const ColorScheme(
          brightness: Brightness.light,
          primary: Colors.brown,
          onPrimary: Colors.white,
          secondary: Colors.white,
          onSecondary: Colors.orange,
          error: Colors.red,
          onError: Colors.white,
          background: Colors.white,
          onBackground: Colors.black,
          surface: Colors.white,
          onSurface: Colors.black,
        ),
      ),
    );
  }
}

class MainPage extends StatefulWidget {
  const MainPage({super.key});

  @override
  State<MainPage> createState() => _MainPageState();
}

class _MainPageState extends State<MainPage> {
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
      body: Center(
        child: Column(
          mainAxisSize: MainAxisSize.max,
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            GradientText(
              'Tu préfères ...',
              style: const TextStyle(fontSize: 40, fontWeight: FontWeight.bold),
              colors: const [
                Colors.brown,
                Colors.orange,
              ],
            ),
            const SizedBox(height: 120),
            ElevatedButton(
              child: const Text('Enregistrement'),
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                      builder: (context) => const RegisterWindow()),
                );
              },
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              child: const Text('Connexion'),
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => const LoginWindow()),
                );
              },
            ),
            const SizedBox(height: 150),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 25),
              child: ElevatedButton(
                onPressed: () {
                  showModalBottomSheet<void>(
                    showDragHandle: true,
                    context: context,
                    builder: (BuildContext context) {
                      return const SizedBox(
                        //height: 1000,
                        child: Center(
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            mainAxisSize: MainAxisSize.min,
                            children: <Widget>[
                              Text('show rules here'),
                              // ElevatedButton(
                              //   child: const Text('Close BottomSheet'),
                              //   onPressed: () => Navigator.pop(context),
                              // ),
                            ],
                          ),
                        ),
                      );
                    },
                  );
                },
                child: const Text('Regles du jeu'),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
