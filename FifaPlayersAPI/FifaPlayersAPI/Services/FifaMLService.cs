using System;
using System.Text;
using System.Collections.Generic;
using System.Net.Http;
using FifaPlayersAPI.Model.Requests;
using Newtonsoft.Json;

namespace FifaPlayersAPI.Services
{
    public class FifaMLService
    {

        private static readonly HttpClient client = new HttpClient();
        private static string Uri = "http://127.0.0.1:5000/api/v1/KNN";

        public ClosestPlayerResponse POST(ClosestPlayerRequest closestPlayerRequest) {

            if (goodRequest(closestPlayerRequest))
            {

                //Body to JSON
                var json = JsonConvert.SerializeObject(closestPlayerRequest);
                var data = new StringContent(json, Encoding.UTF8, "application/json");

                //Get request response and turn into string....
                var obj = client.PostAsync(Uri, data).Result;
                var response = obj.Content.ReadAsStringAsync().Result;
                ClosestPlayerResponse playerResponse = JsonConvert.DeserializeObject<ClosestPlayerResponse>(response);

                return playerResponse;

            }
            else {

                return new ClosestPlayerResponse(new List<long>(), "Bad Request!");
            }       

        }

        private bool goodRequest(ClosestPlayerRequest closestPlayerRequest) { 
            return true;
        }

    }

}
 