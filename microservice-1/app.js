const app=require('express')()
const bodyParser=require('body-parser')

app.use(bodyParser.json())


var amqp = require('amqplib/callback_api');

const url = 'amqp://localhost';
const queue = 'my-queue';

let channel = null;
amqp.connect(url, function (err, conn) {
  if (!conn) {
    throw new Error(`AMQP connection not available on ${url}`);
  }
  conn.createChannel(function (err, ch) {
    channel = ch;
  });
});

app.get("/",(req,res)=>{
    res.send("hello")
})

app.post("/new_ride",(req,res)=>{
    console.log(req.body)
    channel.sendToQueue('my-queue', new Buffer.from(JSON.stringify(req.body)));
    res.send("yo yo")

})
process.on('exit', code => {
    channel.close();
    console.log(`Closing`);
  });

app.post("/new_ride_matching_consumer",(req,res)=>{

})
app.listen(3000,()=>{
    console.log("[+] Server started at 3000")
})

