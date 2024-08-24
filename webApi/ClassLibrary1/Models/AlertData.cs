using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ClassLibrary1.Models
{
    public class AlertData
    {
        public int? AlertNumber { get; set; }
        public string AlertNumberString { get; set; }
        public string County { get; set; }
        public string? District { get; set; } // District 欄位可選
        public string Id { get; set; }
        public int Type { get; set; }
    }
}
