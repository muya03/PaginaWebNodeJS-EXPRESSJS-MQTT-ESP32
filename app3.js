var express = require('express');
const { Client } = require("pg");
var cors = require('cors');
var app = express();
var mqtt = require('mqtt');
var Topic = 'Test/#'; //subscribe to all topics
var Broker_URL = 'mqtt://localhost';

var options = {
    clientId: 'm7003',
    port: 1884,
    keepalive : 60
};


// Configurar cabeceras y cors
app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Headers', 'Authorization, X-API-KEY, Origin, X-Requested-With, Content-Type, Accept, Access-Control-Allow-Request-Method');
    res.header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE');
    res.header('Allow', 'GET, POST, OPTIONS, PUT, DELETE');
    next();
}); 

app.use(express.json());
app.use(cors());



var client  = mqtt.connect(Broker_URL, options);
client.on('connect', mqtt_connect);
client.on('reconnect', mqtt_reconnect);
client.on('error', mqtt_error);
client.on('message', mqtt_messsageReceived);
client.on('close', mqtt_close);

function mqtt_connect()
{
    console.log("Connecting MQTT");
    client.subscribe(Topic, mqtt_subscribe);
}

function mqtt_subscribe(err, granted){
    console.log("Subscribed to " + Topic);
    if (err) {console.log(err);}
}


function mqtt_reconnect(err) {
    console.log("Reconnect MQTT");
    if (err) {console.log(err);}
    client  = mqtt.connect(Broker_URL, options);
}

function mqtt_error(err) {
    console.log("Error!");
    if (err) {console.log(err);}
}

function after_publish(){
    //do nothing
}

function mqtt_messsageReceived(topic, message, packet){
    console.log('Topic=' +  topic + '  Message=' + message);
}

function mqtt_close(){
    console.log("Close MQTT");
}

app.get('/mqtt/datos', (req,res) => {
    (topic + " " + message).then((response => {
        res.send(response.rows)
    }))
});

app.get('/mqtt/datos2', (req,res) => {
    (topic + " " + message).then((response => {
        res.send(response.rows)
        
    }))
});



//Establecemos los prámetros de conexión
//var conexion = mysql.createConnection({
//    host:'localhost',
//    user:'moha',
//    password:'moha',
//    database:'my_db'
//});

//const conexion = new Client({
//    user: "postgres",
//    host: "localhost",
//    database: "my_db",
//    password: "postgres",
//    port: 5432,
//});

//Conexión a la database
//conexion.connect(function(error){
//    if(error){
//        throw error;
//    }else{
//        console.log("¡Conexión exitosa a la base de datos!");
//    }
//});
//app.get('/', function(req,res){
//    res.send('Ruta INICIO');
//});

//Mostrar todos los artículos
//app.get('/my_db/datos', (req,res)=>{
//    conexion.query('SELECT * FROM datos2').then(response => {
//        res.send(response.rows)
//        //conexion.end()
//    })
//});

//Mostrar todos los artículos
//app.get('/my_db/datos3', (req,res)=>{
//    conexion.query('SELECT * FROM datos2').then(response => {
//        res.send(response.rows)
//        //conexion.end()
//    })
//});


//Mostrar todos los artículos
//app.get('/my_db/datos2', (req,res)=>{
//    conexion.query('SELECT * FROM datos2').then(response => {
//        res.send(response.rows)
//        conexion.end()
//    })
//});

const puerto = process.env.PUERTO || 3001;
app.listen(puerto, function(){
    console.log("Servidor Ok en puerto:"+puerto);
});
