using System;
namespace FifaPlayersAPI.Model.Requests
{
    public class ClosestPlayerRequest
    {

        public long playerID { get; set; }

        public long nNeighbors { get; set; }

        public bool ignoreNationality { get; set; }

        public string playerType { get; set;  }

    }
}
