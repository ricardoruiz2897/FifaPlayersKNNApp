using System;
using System.IO;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;

using Json.Net;

using FifaPlayersAPI.Model;
using FifaPlayersAPI.Model.Requests;
using FifaPlayersAPI.Process;


namespace FifaPlayersAPI.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class FifaPlayersController : ControllerBase
    {

        private readonly ILogger<FifaPlayersController> _logger;

        private ProcessClosestPlayerRequest processClosestPlayerRequest;

        public FifaPlayersController(ILogger<FifaPlayersController> logger)
        {
            _logger = logger;
        }

        [HttpGet]
        public Dictionary<string, List<PlayerInfo>> Get()
        {
            using (StreamReader r = System.IO.File.OpenText("Data/front_end_dataset.json"))
            {
                string json = r.ReadToEnd();

                var  dic = new Dictionary<string, List<PlayerInfo>>()
                {
                    { "players",  JsonNet.Deserialize<List<PlayerInfo>>(json) }
            
                };

                return dic;
            }

        }

        [HttpPost]
        public IEnumerable<PlayerInfo> ClosestPlayerPost([FromBody] ClosestPlayerRequest request)
        {
            processClosestPlayerRequest = new ProcessClosestPlayerRequest();
            return processClosestPlayerRequest.process(request);
        }
    }
}
