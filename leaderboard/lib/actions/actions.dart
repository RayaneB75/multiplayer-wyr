import '/backend/api_requests/api_calls.dart';
import '/backend/api_requests/api_manager.dart';
import '/backend/backend.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

Future refreshData(BuildContext context) async {
  ApiCallResponse? apiResulthlu;

  while (true) {
    apiResulthlu = await DashboardCall.call();
    if ((apiResulthlu?.succeeded ?? true)) {
      FFAppState().resApi = (apiResulthlu?.jsonBody ?? '');
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
            'Vérifiez l\'accessibilité de l\'API',
            style: TextStyle(),
          ),
          duration: Duration(milliseconds: 4000),
          backgroundColor: FlutterFlowTheme.of(context).secondary,
        ),
      );
    }

    await Future.delayed(const Duration(milliseconds: 10000));
  }
}
