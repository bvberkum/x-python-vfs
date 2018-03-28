@test "Not mounted" {
  mount | grep -v '\/tmp\/x-fuse'
}
