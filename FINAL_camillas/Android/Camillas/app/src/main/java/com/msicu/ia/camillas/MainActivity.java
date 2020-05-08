package com.msicu.ia.camillas;

import android.preference.PreferenceManager;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        final Spinner spinner = (Spinner) findViewById(R.id.sick);
        ArrayAdapter<CharSequence> adapter = ArrayAdapter.createFromResource(this,
                R.array.sick_array, android.R.layout.simple_spinner_item);
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        spinner.setAdapter(adapter);

        final LinearLayout lls = findViewById(R.id.savev);
        final LinearLayout llr = findViewById(R.id.readv);

        final RequestQueue queue = Volley.newRequestQueue(this);
        String url = "http://192.168.1.124:5000/patient/read";
        StringRequest stringRequest = new StringRequest(Request.Method.POST, url,
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        Log.d("REQUESTS",response);
                        if (response.contains("NOPATIENT")){
                            lls.setVisibility(View.VISIBLE);
                        }else {
                            TextView txt1 = findViewById(R.id.namev);
                            TextView txt2 = findViewById(R.id.agev);
                            TextView txt3 = findViewById(R.id.sickv);
                            llr.setVisibility(View.VISIBLE);
                            try {
                                JSONObject jsonobj = new JSONObject(response);
                                txt1.setText(jsonobj.getString("name"));
                                txt2.setText(jsonobj.getString("age"));
                                switch (jsonobj.getString("sick")){
                                    case "respiratory":
                                        txt3.setText("Respiratoria");
                                        break;
                                    case "heatstroke":
                                        txt3.setText("Por Calor");
                                        break;
                                    case "hypothermia":
                                        txt3.setText("Por Frio");
                                        break;
                                    case "other":
                                        txt3.setText("Otra");
                                        break;
                                }
                            } catch (JSONException e) {
                                e.printStackTrace();
                            }

                        }
                    }
                }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                Log.i("REQUESTS","Error :" + error.toString());
            }
        }){
            @Override
            public Map<String,String> getParams() {
                HashMap<String, String> params = new HashMap<String, String>();
                String valdf = PreferenceManager.getDefaultSharedPreferences(getApplicationContext()).getString("NAME", "");
                params.put("name", valdf);

                return params;
            }
        };

        queue.add(stringRequest);

        Button btns = findViewById(R.id.save);
        btns.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                final EditText edt1 = findViewById(R.id.name);
                final EditText edt2 = findViewById(R.id.age);
                final TextView txt1 = findViewById(R.id.namev);
                final TextView txt2 = findViewById(R.id.agev);
                final TextView txt3 = findViewById(R.id.sickv);


                String url = "http://192.168.1.124:5000/patient/save";
                StringRequest stringRequestsave = new StringRequest(Request.Method.POST, url,
                        new Response.Listener<String>() {
                            @Override
                            public void onResponse(String response) {
                                Log.d("REQUESTS",response);
                                if (response.contains("saved")){
                                    lls.setVisibility(View.GONE);
                                    llr.setVisibility(View.VISIBLE);
                                    txt1.setText(edt1.getText().toString());
                                    txt2.setText(edt2.getText().toString());
                                    txt3.setText(spinner.getSelectedItem().toString());
                                    PreferenceManager.getDefaultSharedPreferences(getApplicationContext()).edit().putString("NAME", edt1.getText().toString()).apply();
                                }else {
                                    Toast.makeText(getApplicationContext(),"Error al guardar, intente de nuevo",Toast.LENGTH_SHORT).show();
                                }
                            }
                        }, new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Log.i("REQUESTS","Error :" + error.toString());
                    }
                }){
                    @Override
                    public Map<String,String> getParams() {
                        HashMap<String, String> params = new HashMap<String, String>();
                        params.put("name", edt1.getText().toString());
                        params.put("age", edt2.getText().toString());
                        switch (spinner.getSelectedItem().toString()){
                            case "Respiratoria":
                                params.put("sick","respiratory");
                                break;
                            case "Por Calor":
                                params.put("sick","heatstroke");
                                break;
                            case "Por Frio":
                                params.put("sick","hypothermia");
                                break;
                            case "Otra":
                                params.put("sick","other");
                                break;
                        }

                        return params;
                    }
                };
                queue.add(stringRequestsave);
            }
        });

        Button btnr = findViewById(R.id.delete);
        btnr.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                final EditText edt1 = findViewById(R.id.name);
                final EditText edt2 = findViewById(R.id.age);
                final TextView txt1 = findViewById(R.id.namev);
                final TextView txt2 = findViewById(R.id.agev);
                final TextView txt3 = findViewById(R.id.sickv);


                String url = "http://192.168.1.124:5000/patient/delete";
                StringRequest stringRequestdelete = new StringRequest(Request.Method.POST, url,
                        new Response.Listener<String>() {
                            @Override
                            public void onResponse(String response) {
                                Log.d("REQUESTS",response);
                                if (response.contains("retracted")){
                                    lls.setVisibility(View.VISIBLE);
                                    llr.setVisibility(View.GONE);
                                    edt1.setText("");
                                    edt2.setText("");
                                    spinner.setSelection(0);
                                    PreferenceManager.getDefaultSharedPreferences(getApplicationContext()).edit().putString("NAME", "").apply();
                                }else {
                                    Toast.makeText(getApplicationContext(),"Error al eliminar, intente de nuevo",Toast.LENGTH_SHORT).show();
                                }
                            }
                        }, new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Log.i("REQUESTS","Error :" + error.toString());
                    }
                }){
                    @Override
                    public Map<String,String> getParams() {
                        HashMap<String, String> params = new HashMap<String, String>();
                        String valdf = PreferenceManager.getDefaultSharedPreferences(getApplicationContext()).getString("NAME", "");
                        params.put("name", valdf);

                        return params;
                    }
                };
                queue.add(stringRequestdelete);
            }
        });
    }
}
