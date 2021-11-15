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

// Homerico Get Gateway Ip
await homerico.validar(process.env.HOMERICO_GATEWAY)

// Homerico Authentication
await homerico.login({
  usuario: process.env.HOMERICO_USER,
  senha: process.env.HOMERICO_PASSWORD
})

/*
##########################################################################################################################
#                                                          MAIN                                                          #
##########################################################################################################################
*/

// Set Network API
const app = express()

// Set Network API Port
const port = Number(process.env.HOMERICO_SERVICE_PORT)

/*
##########################################################################################################################
*/

// Homerico Ignore Items
const ignore = ['acesso', 'relatorio', 'validar', 'login'] as const
const keys = Object.getOwnPropertyNames(HomericoConexao.prototype)

// Iterate over Homerico Methods
keys.forEach(item => {
  // Check for Valid Item
  if (item in ignore) return
  // Post Endnode
  app.post(
    `/homerico/${item}`,
    express.json() as RequestHandler,
    async (req, res) => {
      // log action to be executed
      const ip = requestIp.getClientIp(req).replace('::ffff:', '')
      misc.logging.log(`Exec(homerico::${item}) From(${ip})`)
      // check request
      if (!is.object(req)) throw new Error('bad request')
      if (!is.in(req, 'body', 'object')) throw new Error('bad request')
      // Execute Function
      const data = await homerico[item](req.body)
      // Send Response
      res.send(data)
    }
  )
})

/*
##########################################################################################################################
*/

// Listen on Port Especified
app.listen(port)

// Log Bot Start
misc.logging.log('homerico::started')

/*
##########################################################################################################################
#                                                          END                                                           #
##########################################################################################################################
*/
