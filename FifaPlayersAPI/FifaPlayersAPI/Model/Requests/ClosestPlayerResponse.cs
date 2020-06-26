using System;
using System.Collections.Generic;

namespace FifaPlayersAPI.Model.Requests
{
    public class ClosestPlayerResponse
    {

        public ClosestPlayerResponse() { }

        public ClosestPlayerResponse(List<long> ids, string message) {
            this.ids = ids;
            this.message = message;
        }

        public ClosestPlayerRequest request;

        public List <long> ids { get; set; }

        public string message { get; set; }

    }
}
