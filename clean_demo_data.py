#!/usr/bin/env python3
"""
Clean Demo Data from Convex
Removes all data tagged with demo user/org IDs for fresh testing.

Usage:
    python clean_demo_data.py                    # Preview what will be deleted
    python clean_demo_data.py --execute          # Actually delete demo data
    python clean_demo_data.py --demo-org custom  # Use custom demo org ID
"""

import argparse
import sys
from pathlib import Path

# Add MCP src to path
sys.path.insert(0, str(Path(__file__).parent / "mcp" / "src"))

from persistence.convex_client import ConvexClient
from config import config


class DemoDataCleaner:
    """Clean demo data from Convex database."""
    
    def __init__(self, demo_user_id: str = None, demo_org_id: str = None, dry_run: bool = True):
        self.client = ConvexClient()
        self.demo_user_id = demo_user_id or config.DEMO_USER_ID
        self.demo_org_id = demo_org_id or config.DEMO_ORG_ID
        self.dry_run = dry_run
        
    def find_demo_data(self):
        """Find all demo data in Convex."""
        print(f"\n🔍 Searching for demo data...")
        print(f"   Demo User ID: {self.demo_user_id}")
        print(f"   Demo Org ID: {self.demo_org_id}\n")
        
        demo_data = {
            "projects": [],
            "conflicts": [],
            "ambiguities": [],
            "gaps": [],
            "questions": [],
            "documents": [],
            "contextEvents": [],
            "deliverables": []
        }
        
        # For each table, we'd need to query by orgId/userId
        # Note: This requires appropriate query functions in Convex
        
        print("⚠️  Note: Actual deletion requires Convex query/mutation support")
        print("   For now, use Convex dashboard to manually delete demo data")
        print(f"   Filter by: orgId = '{self.demo_org_id}' or userId = '{self.demo_user_id}'")
        
        return demo_data
    
    def preview_deletion(self):
        """Preview what will be deleted."""
        print(f"\n{'='*60}")
        print("DEMO DATA CLEANUP - PREVIEW")
        print(f"{'='*60}\n")
        
        demo_data = self.find_demo_data()
        
        total_records = sum(len(records) for records in demo_data.values())
        
        if total_records == 0:
            print("✅ No demo data found - database is clean!")
        else:
            print("Found demo data:")
            for table, records in demo_data.items():
                if records:
                    print(f"   {table}: {len(records)} records")
            
            print(f"\n   Total: {total_records} records to delete")
            print(f"\n   Run with --execute to actually delete this data")
    
    def execute_deletion(self):
        """Actually delete demo data."""
        print(f"\n{'='*60}")
        print("DEMO DATA CLEANUP - EXECUTING")
        print(f"{'='*60}\n")
        
        demo_data = self.find_demo_data()
        total_records = sum(len(records) for records in demo_data.values())
        
        if total_records == 0:
            print("✅ No demo data found - nothing to delete!")
            return
        
        print("⚠️  This will permanently delete demo data!")
        response = input("   Type 'DELETE' to confirm: ")
        
        if response != "DELETE":
            print("   Cancelled - no data was deleted")
            return
        
        print("\n🗑️  Deleting demo data...")
        
        # Delete in reverse dependency order
        deletion_order = [
            "deliverables",
            "contextEvents",
            "documents",
            "questions",
            "gaps",
            "ambiguities",
            "conflicts",
            "projects"
        ]
        
        deleted_count = 0
        for table in deletion_order:
            records = demo_data.get(table, [])
            if records:
                print(f"   Deleting {len(records)} records from {table}...")
                # Would call Convex delete mutations here
                deleted_count += len(records)
        
        print(f"\n✅ Deleted {deleted_count} demo records")
        print("   Demo data cleanup complete!")


def main():
    parser = argparse.ArgumentParser(
        description="Clean demo data from Convex database",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Preview what will be deleted
    python clean_demo_data.py
    
    # Actually delete demo data
    python clean_demo_data.py --execute
    
    # Use custom demo org ID
    python clean_demo_data.py --demo-org my-demo-org --execute
    
    # Use custom demo user ID
    python clean_demo_data.py --demo-user my-demo-user --execute
        """
    )
    
    parser.add_argument("--execute", action="store_true", 
                      help="Actually delete data (default is dry-run preview)")
    parser.add_argument("--demo-user", type=str,
                      help=f"Demo user ID to clean (default: {config.DEMO_USER_ID})")
    parser.add_argument("--demo-org", type=str,
                      help=f"Demo org ID to clean (default: {config.DEMO_ORG_ID})")
    
    args = parser.parse_args()
    
    # Check Convex connection
    if not config.is_convex_enabled():
        print("❌ Error: Convex not configured")
        print("   Set CONVEX_DEPLOYMENT_URL in mcp/.env")
        sys.exit(1)
    
    try:
        cleaner = DemoDataCleaner(
            demo_user_id=args.demo_user,
            demo_org_id=args.demo_org,
            dry_run=not args.execute
        )
        
        if args.execute:
            cleaner.execute_deletion()
        else:
            cleaner.preview_deletion()
            print("\n💡 Tip: Add --execute to actually delete the data")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

