
import 'package:flutter/material.dart';

// email field
class TextFieldCustom extends StatefulWidget {

    final String content;
    final TextEditingController controller;

    const TextFieldCustom({Key? key, required this.content, required this.controller}) : super(key: key);

  @override
  State<TextFieldCustom> createState() => _TextFieldCustomState();
}

class _TextFieldCustomState extends State<TextFieldCustom> {

  @override
  Widget build(BuildContext context) {
      return Padding(
        padding: const EdgeInsets.symmetric(horizontal: 30, vertical: 16),
        child: TextFormField(
          validator: (value) {
              if (value == null || value.isEmpty) {
                return 'S\'il vous plait renseignez ce champ';
              } else if (!value.endsWith("@imt-atlantique.net")) {
                return 'E-mail invalide (prenom.nom@imt-atlantique.net)';
              }
              return null;
            },
          controller: widget.controller,
          decoration: InputDecoration(
            border: const OutlineInputBorder(),
            labelText: widget.content,
          ),
        ),
      );
  }
}

// password field
class PasswordFieldCustom extends StatefulWidget {

    final String content;
    final TextEditingController controller;

    const PasswordFieldCustom({Key? key, required this.content, required this.controller}) : super(key: key);

  @override
  State<PasswordFieldCustom> createState() => _PasswordFieldCustomState();
}

class _PasswordFieldCustomState extends State<PasswordFieldCustom> {

  // Initially password is obscure
  bool _obscureText = true;

  @override
  Widget build(BuildContext context) {
      return Padding(
        padding: const EdgeInsets.symmetric(horizontal: 30, vertical: 16),
        child: TextFormField(
          validator: (value) {
              if (value == null || value.isEmpty) {
                return 'S\'il vous plait renseignez ce champ';
              } else if (value.length < 8) {
                return 'Le mot de passe est trop court';
              }
              return null;
            },
          controller: widget.controller,
          obscureText: _obscureText,
          decoration: InputDecoration(
            border: const OutlineInputBorder(),
            labelText: widget.content,
            suffixIcon: IconButton(
            icon: Icon(
              // Based on passwordVisible state choose the icon
               _obscureText
               ? Icons.visibility
               : Icons.visibility_off,
               ),
            onPressed: () {
               // Update the state i.e. toogle the state of passwordVisible variable
               setState(() {
                   _obscureText = !_obscureText;
               });
             },
            ),

          ),
        ),
      );
  }
}
