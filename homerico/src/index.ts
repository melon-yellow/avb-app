/*
##########################################################################################################################
#                                                      AVB-HOMERICO                                                      #
##########################################################################################################################
#                                                                                                                        #
#                                                  Homerico Conexão AVB                                                  #
#                                            Multi-language API for Homerico                                             #
#                                  ---------------- Python3 -- NodeJS ----------------                                   #
#                                                 * Under Development *                                                  #
#                                      https://github.com/anthony-freitas/avb-app                                        #
#                                                                                                                        #
##########################################################################################################################
#                                                        MAIN CODE                                                       #
##########################################################################################################################
*/

// Import Homerico
import HomericoConexao from 'ts-homerico'

// Import Super-Guards
import Miscellaneous from 'ts-misc'
import { is } from 'ts-misc/dist/utils/guards.js'

// Import Express
import express, { RequestHandler } from 'express'
import basicAuth from 'express-basic-auth'
import requestIp from 'request-ip'

// Instance Miscellaneous
const misc = new Miscellaneous()

/*
##########################################################################################################################
#                                                          MAIN                                                          #
##########################################################################################################################
*/

// Instance Homerico
const homerico = new HomericoConexao()

// Homerico Authentication
await homerico.validar(process.env.HOMERICO_GATEWAY)
await homerico.login({
  usuario: process.env.HOMERICO_USER,
  senha: process.env.HOMERICO_PASSWORD
})

/*
##########################################################################################################################
#                                                          MAIN                                                          #
##########################################################################################################################
*/

// Set App
const app = express()
app.use(express.json() as RequestHandler)

// Homerico Ignore Items
const ignore = ['acesso', 'relatorio', 'validar', 'login'] as const
const keys = Object.getOwnPropertyNames(HomericoConexao.prototype)

// Iterate over Homerico Methods
keys.forEach(item => {
  // Check for Valid Item
  if (item in ignore) return
  // Post Endnode
  app.post(`/homerico/${item}`, async (req, res) => {
    // log action to be executed
    const ip = requestIp.getClientIp(req).replace('::ffff:', '')
    misc.logging.log(`Exec(homerico::${item}) From(${ip})`)
    // check request
    if (!is.object(req)) throw new Error('bad request')
    if (!is.object(req.body)) throw new Error('bad request')
    // Execute Function
    const data = await homerico[item](req.body)
    // Send Response
    res.send(data)
  })
})

/*
##########################################################################################################################
#                                                          MAIN                                                          #
##########################################################################################################################
*/

// Set Authentication
app.use(
  basicAuth({
    users: {
      [process.env.HOMERICO_NETWORK_USER]: (
        process.env.HOMERICO_NETWORK_PASSWORD
      )
    }
  })
)

// Listen on Port Especified
app.listen(
  Number(process.env.HOMERICO_NETWORK_PORT)
)

// Log Bot Start
misc.logging.log('homerico::started')

/*
##########################################################################################################################
#                                                          END                                                           #
##########################################################################################################################
*/
