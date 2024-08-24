using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ClassLibrary1.Models
{
    public class PythonRequest
    {
        public Dictionary<int, List<AlertData>> Images { get; set; }
        //public List<AlertData>? AlertsData { get; set; }
    }
}
