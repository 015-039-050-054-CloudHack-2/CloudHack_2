const app=require('express')()
const bodyParser=require('body-parser')

app.use(bodyParser.json())


var amqp = require('amqplib/callback_api');

console.log(process.env.AMQP_HOST)

const url = `amqp://rabbitmq-container`;
const queue = process.env.QUEUE_NAME;

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
    channel.sendToQueue('data-queue', new Buffer.from(JSON.stringify(req.body)));
    res.send("yo yo")

})
process.on('exit', code => {
    channel.close();
    console.log(`Closing`);
  });

app.post("/new_ride_matching_consumer",(req,res)=>{
  console.log(req.body)
  // channel.sendToQueue('data-queue', new Buffer.from(JSON.stringify(req.body)));
  res.send("consumer registered!")
})

app.listen(3000,()=>{
    console.log("[+] Server started at 3000")
})


// app.get("/",(req,res)=>{
//   console.log("api   was hit")
//     res.send("hello")
// })
// app.post("/new_ride_matching_consumer",(req,res)=>{
//   console.log(req.body)
//   // channel.sendToQueue('data-queue', new Buffer.from(JSON.stringify(req.body)));
//   res.send("data added to queue")
// })
// app.listen(3000,()=>{
//     console.log("[+] Server started at 3000")
// })

