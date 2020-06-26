using System;
using System.Linq;
using System.Collections.Generic;
using System.IO;

using FifaPlayersAPI.Model;
using FifaPlayersAPI.Model.Requests;
using FifaPlayersAPI.Services;

using Json.Net;

namespace FifaPlayersAPI.Process
{
    public class ProcessClosestPlayerRequest
    {

        private FifaMLService fifaMLService;

        public ProcessClosestPlayerRequest() {
            fifaMLService = new FifaMLService();
        }

        public List<PlayerInfo> process(ClosestPlayerRequest request) {

            //Make the request
            ClosestPlayerResponse closestPlayerResponse = fifaMLService.POST(request);

            //Response list id empty
            if (closestPlayerResponse.ids.Count == 0) {
                return new List<PlayerInfo>();
            }

            //Load all the players, and filter the players in the list.
            using (StreamReader r = System.IO.File.OpenText("Data/front_end_dataset.json"))
            {
                string json = r.ReadToEnd();
                List<PlayerInfo> allPlayers = JsonNet.Deserialize<List<PlayerInfo>>(json);

                //Filter players in response..
                List<PlayerInfo> filtered = allPlayers.Where(player => closestPlayerResponse.ids.Contains(player.id)).ToList();


                return filtered;
            }

        }
      
    }
}
